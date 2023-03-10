# See here for image contents: https://github.com/microsoft/vscode-dev-containers/tree/v0.241.1/containers/ubuntu/.devcontainer/base.Dockerfile

# [Choice] Ubuntu version (use ubuntu-22.04 or ubuntu-18.04 on local arm64/Apple Silicon): ubuntu-22.04, ubuntu-20.04, ubuntu-18.04
ARG VARIANT="focal"

FROM mcr.microsoft.com/vscode/devcontainers/base:0-${VARIANT} AS build_valgrind
# Install valgrind patched to add support for SGX simulation
RUN apt-get update \
    && apt-get install -y autotools-dev automake \
    && git clone --depth 1 -b sgx https://github.com/mithril-security/valgrind.git \
    && cd valgrind \
    && ./autogen.sh \
    && ./configure \
    && make

## Final image
FROM mcr.microsoft.com/vscode/devcontainers/base:0-${VARIANT} AS development
# [Optional] Uncomment this section to install additional OS packages.
# RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
#     && apt-get -y install --no-install-recommends <your-package-list-here>

ENV CARGO_HOME=/usr/local/cargo \
    RUSTUP_HOME=/usr/local/rustup \
    POETRY_HOME=/home/vscode/.local/bin
ENV PATH=${CARGO_HOME}/bin:${POETRY_HOME}:${PATH}
COPY .devcontainer/library-scripts/rust-debian.sh /tmp/library-scripts/

# Enable default rustup profile instead of the minimal profile (default of the rust-debian.sh)
# The default profile includes all of components in the minimal profile, and adds rust-docs, rustfmt, and clippy. 
# This profile will be used by rustup by default, and it's the one recommended for general use.
RUN apt-get update && bash /tmp/library-scripts/rust-debian.sh "${CARGO_HOME}" "${RUSTUP_HOME}" "" "" "" "" "default"

RUN echo "deb https://download.01.org/intel-sgx/sgx_repo/ubuntu $(lsb_release -cs) main" | tee -a /etc/apt/sources.list.d/intel-sgx.list >/dev/null \ 
    && curl -sSL "https://download.01.org/intel-sgx/sgx_repo/ubuntu/intel-sgx-deb.key" | apt-key add - \
    && apt-get update \
    && apt-get install -y sgx-aesm-service libsgx-aesm-launch-plugin

RUN rustup default nightly \
    && rustup target add x86_64-fortanix-unknown-sgx --toolchain nightly \
    && chmod -R g+r+w "${RUSTUP_HOME}"
    
RUN apt-get update \
    && apt-get install -y pkg-config libssl-dev protobuf-compiler

# Fix #1 We need to download and install from fortanix git repo instead of crates.io becaue of this issue 
# https://github.com/fortanix/rust-sgx/issues/401
# Fix #2 To enable simulation mode we use our own fork
RUN cargo install fortanix-sgx-tools ftxsgx-simulator sgxs-tools --git https://github.com/mithril-security/rust-sgx --branch sim-mode \
    && chmod -R g+r+w "${CARGO_HOME}"

# Add valgrind
COPY --from=build_valgrind /valgrind /valgrind
RUN apt-get install -y automake \
    &&  cd /valgrind \
    && make install

# Add gdb
RUN apt-get install -y gdb

# Add just
RUN curl --proto '=https' --tlsv1.2 -sSf https://just.systems/install.sh | bash -s -- --to /usr/bin

# Add poetry and python dev utilities
RUN apt-get install -y python3-dev python3-distutils python3-pip \
    && sudo -u "vscode" zsh -c "\
    curl -sSL https://install.python-poetry.org | python3 - \
    && mkdir ~/.oh-my-zsh/custom/plugins/poetry \
    && export PATH=${POETRY_HOME}:$PATH \
    && poetry completions zsh > ~/.oh-my-zsh/custom/plugins/poetry/_poetry \
    && sed -i -E 's/^plugins\=\(([a-zA-Z ]+)*\)/plugins=(\1 poetry)/' ~/.zshrc" \
    && pip install black mypy

# Add github cli
RUN curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg \
    && chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null \
    && apt update \
    && apt install gh -y

RUN apt-get install -y software-properties-common \
    && curl -fsSL  https://download.01.org/intel-sgx/sgx_repo/ubuntu/intel-sgx-deb.key | apt-key add - \
    && add-apt-repository "deb https://download.01.org/intel-sgx/sgx_repo/ubuntu $(lsb_release -cs) main" \
    && apt-get install -y libsgx-dcap-ql-dev libsgx-dcap-default-qpl-dev libsgx-uae-service libsgx-dcap-default-qpl
    # TODO: Do we still need the symbolic link hack ?
    # sudo ln -s /usr/lib/x86_64-linux-gnu/libdcap_quoteprov.so.1 /usr/lib/x86_64-linux-gnu/libdcap_quoteprov.so 
    # Remove temp dependencies
    # apt-get remove -y $TEMP_DEPENDENCIES && apt-get autoremove -y && \
    # rm -rf /var/lib/apt/lists/* && rm -rf /var/cache/apt/archives/*

RUN apt-get install -y \
    libcurl4 \
    libssl1.1 \
    make \
    cmake \
    libpython3.8-dev

# PCCS 
RUN curl -sL https://deb.nodesource.com/setup_16.x | bash - \
    && apt-get install -y nodejs cracklib-runtime \
    && npm install -g esm pm2 

RUN git clone https://github.com/intel/SGXDataCenterAttestationPrimitives.git \
    && make -C SGXDataCenterAttestationPrimitives/tools/PCKCertSelection/ \
    && mkdir -p SGXDataCenterAttestationPrimitives/QuoteGeneration/pccs/lib/ \
    && cp SGXDataCenterAttestationPrimitives/tools/PCKCertSelection/out/libPCKCertSelection.so SGXDataCenterAttestationPrimitives/QuoteGeneration/pccs/lib/ \
    && cp -R SGXDataCenterAttestationPrimitives/QuoteGeneration/pccs/ /opt/intel/sgx-dcap-pccs \
    && sed -i 's/"use_secure_cert": true/"use_secure_cert": false/g' /etc/sgx_default_qcnl.conf   

COPY .devcontainer/setup-pccs.sh /opt/intel/sgx-dcap-pccs/setup-pccs.sh
COPY .devcontainer/hw-start.sh /opt/intel/sgx-dcap-pccs/hw-start.sh
COPY .devcontainer/default.json /opt/intel/sgx-dcap-pccs/default.json

RUN /opt/intel/sgx-dcap-pccs/setup-pccs.sh

# Add examples dependencies
RUN apt-get install -y ffmpeg

# Add cargo audit
RUN cargo install cargo-audit
# Install Earthly
RUN wget https://github.com/earthly/earthly/releases/latest/download/earthly-linux-amd64 -O /usr/local/bin/earthly \ 
    && chmod +x /usr/local/bin/earthly \
    && /usr/local/bin/earthly bootstrap --with-autocomplete

COPY .earthly/config.yml /home/vscode/.earthly/config.yml