# Minimal image to build the release version of the sgx enclave
FROM rust:1.66.1-slim-bullseye as build-sgxs
WORKDIR blindai-preview

ENV BIN_PATH=target/x86_64-fortanix-unknown-sgx/release/blindai_server

# Install dependencies and pre-install the rust toolchain declared via rust-toolchain.toml 
# for better caching
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        protobuf-compiler=3.12.4-1 \
        pkg-config=0.29.2-1 \
        libssl-dev=1.1.1n-0+deb11u3 \
        gettext-base \
    && rm -rf /var/lib/apt/lists/* \
    && rustup default nightly-2023-01-11 \
    && rustup target add x86_64-fortanix-unknown-sgx

RUN cargo install --locked --git https://github.com/mithril-security/rust-sgx.git --tag fortanix-sgx-tools_v0.5.1-mithril fortanix-sgx-tools sgxs-tools

COPY Cargo.toml Cargo.lock rust-toolchain.toml  manifest.prod.template.toml ./
COPY .cargo .cargo
COPY src src
COPY tar-rs-sgx tar-rs-sgx
COPY tract tract
COPY ring-fortanix ring-fortanix
COPY tiny-http tiny-http
COPY rouille rouille

RUN cargo build --locked --release --target "x86_64-fortanix-unknown-sgx"

RUN ftxsgx-elf2sgxs "$BIN_PATH" --heap-size 0xFBA00000 --stack-size 0x400000 --threads 20 \
    && mr_enclave=`sgxs-hash "${BIN_PATH}.sgxs"` envsubst < manifest.prod.template.toml > manifest.toml

RUN openssl genrsa -3 3072 > throw_away.pem \
  && sgxs-sign --key throw_away.pem "${BIN_PATH}.sgxs" "${BIN_PATH}.sig" --xfrm 7/0 --isvprodid 0 --isvsvn 0 \
  && rm throw_away.pem

# Build runner
FROM ubuntu:20.04 AS build-runner

ENV PATH=/root/.cargo/bin:$PATH

# Install rust 1.66.1 to stay in sync with sgxs-build
RUN apt-get update \
    && apt-get install -y curl build-essential \
    && curl https://sh.rustup.rs -sSf | bash -s -- -y --default-toolchain=nightly-2023-01-10 --profile=minimal

# Install dcap
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y gnupg2 software-properties-common \
    && curl -fsSL  https://download.01.org/intel-sgx/sgx_repo/ubuntu/intel-sgx-deb.key | apt-key add - \
    && add-apt-repository "deb https://download.01.org/intel-sgx/sgx_repo/ubuntu $(lsb_release -cs) main" \
    && apt-get update && apt-get install -y libsgx-dcap-ql-dev libsgx-dcap-default-qpl-dev libsgx-uae-service libsgx-dcap-default-qpl

# Install runner dependencies
RUN apt-get install -y libssl-dev protobuf-compiler pkg-config

COPY runner runner

RUN cd runner \
    && cargo build --locked --release


# Minimal image to run blindai
FROM ubuntu:20.04 as run-sgx

WORKDIR /root

COPY .devcontainer/setup-pccs.sh /root/

RUN \
    # Install temp dependencies
    TEMP_DEPENDENCIES="git curl make build-essential gcc g++ lsb-release zip" \
    && apt-get update -y && apt-get install -y $TEMP_DEPENDENCIES \

    # Install aesmd
    && echo "deb https://download.01.org/intel-sgx/sgx_repo/ubuntu $(lsb_release -cs) main" | tee -a /etc/apt/sources.list.d/intel-sgx.list >/dev/null \
    && curl -sSL "https://download.01.org/intel-sgx/sgx_repo/ubuntu/intel-sgx-deb.key" | apt-key add - \

    # Install nodejs (needed for PCCS)
    && curl -sL https://deb.nodesource.com/setup_14.x | bash - \
    && apt-get install --no-install-recommends -y nodejs cracklib-runtime \

    # Install DCAP PCCS
    && apt-get install -y libsgx-uae-service libsgx-dcap-default-qpl \
    && git clone https://github.com/intel/SGXDataCenterAttestationPrimitives.git \
    && make -C SGXDataCenterAttestationPrimitives/tools/PCKCertSelection/ \
    && mkdir -p SGXDataCenterAttestationPrimitives/QuoteGeneration/pccs/lib/ \
    && cp SGXDataCenterAttestationPrimitives/tools/PCKCertSelection/out/libPCKCertSelection.so SGXDataCenterAttestationPrimitives/QuoteGeneration/pccs/lib/ \
    && cp -R SGXDataCenterAttestationPrimitives/QuoteGeneration/pccs/ /opt/intel/sgx-dcap-pccs \
    && sed -i 's/"use_secure_cert": true/"use_secure_cert": false/g' /etc/sgx_default_qcnl.conf \
    
    # Install needed nodejs packages
    && npm install -g esm pm2 \

    # Run setup script
    && /root/setup-pccs.sh \

    # Remove temp dependencies
    && apt-get remove -y $TEMP_DEPENDENCIES && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/* && rm -rf /var/cache/apt/archives/*

ENV LD_LIBRARY_PATH=/opt/sgxsdk/sdk_libs:/usr/lib:/usr/local/lib:/opt/intel/sgx-aesm-service/aesm/

COPY .devcontainer/hw-start.sh /root/start.sh

COPY --from=build-sgxs \
    /blindai-preview/target/x86_64-fortanix-unknown-sgx/release/blindai_server.sgxs \
    /blindai-preview/target/x86_64-fortanix-unknown-sgx/release/blindai_server.sig \
    /root

COPY --from=build-runner \
    /runner/target/release/runner /root

EXPOSE 9923
EXPOSE 9924

CMD ./start.sh
