## On-premise deployment

### Eligibility check

In order to deploy BlindAI on-premise, you will need an Intel SGX-ready device with `SGX+FLC` support.

You can check this with the following code:

  ```bash
  git clone https://github.com/ayeks/SGX-hardware
  cd SGX-hardware
  gcc test-sgx.c -o test-sgx
  ./test-sgx | grep "sgx launch control"
  ```

- If your output is `sgx launch control: 1`, you have an Intel SGX-ready device with `SGX+FLC` support.
- If your output is `sgx launch control: 0`, you do not have an Intel SGX-ready device with `SGX+FLC` support.

BlindAI was created for SGX2, which has a better performance and much more memory available than SGX1. The physical protected memory for SGX1 is limited to 128mb.

You could still deploy the server with SGX1 and benefit from the isolation offered by SGX enclaves, but since SGX1 is missing some of the features we rely on, the client would still need to `connect` to the server in `simulation` mode.

You can check if you have SGX1 or SGX2, bu running the following:

```bash
git clone https://github.com/ayeks/SGX-hardware
cd SGX-hardware
gcc test-sgx.c -o test-sgx
./test-sgx | grep "sgx 1 supported"
```

- If your output is `sgx 1 supported: 1`, you have SGX1.
- If your output is `sgx 1 supported: 0`, you do not have SGX1.

```bash
./test-sgx | grep "sgx 2 supported"
```

- If your output is `sgx 2 supported: 1`, you have SGX2.
- If your output is `sgx 2 supported: 0`, you do not have SGX2.

### Intel SGX drivers

>In some cases (Linux kernel >5.15) the execution of the binary returns `in-kernel drivers support`, and it means that the drivers are already installed and must appear in `/dev/sgx/`. 

Please make sure to have the `SGX+FLC` drivers (preferably with version **1.41**) installed on your system before continuing.

✅ If you find the drivers named "enclave" and "provision" (or sgx\_enclave and sgx\_provision) in /dev/, you are good to go!

❌ If you find a driver named "isgx" in /dev/, your system uses SGX1. You could still deploy the server with SGX1 and benefit from the isolation offered by SGX enclaves, but since SGX1 is missing some of the features we rely on, the client would still need to `connect` to the server in `simulation` mode.

If you have an Intel SGX-ready device but are missing the required drivers, you can install them by doing the following:

```bash
wget https://download.01.org/intel-sgx/sgx-linux/2.15.1/distro/ubuntu18.04-server/sgx_linux_x64_driver_1.41.bin
chmod +x sgx_linux_x64_driver_1.41.bin
./sgx_linux_x64_driver_1.41.bin
```

The binary file contains the drivers signed by Intel and will proceed to the installation transparently.


### Server deployment in three steps

1. You firstly need to install and run the `aesm` service which allows our host machine to communicate with the enclave.

You can do this on ubuntu with the following steps:

```bash
# download aesm for ubuntu
echo "deb https://download.01.org/intel-sgx/sgx_repo/ubuntu $(lsb_release -cs) main" | sudo tee -a /etc/apt/sources.list.d/intel-sgx.list >/dev/null \ 
# add to apt-key list to authenticate package
curl -sSL "https://download.01.org/intel-sgx/sgx_repo/ubuntu/intel-sgx-deb.key" | sudo apt-key add -
# update available packages
sudo apt-get update \
# install aesm package
sudo apt-get install -y sgx-aesm-service libsgx-aesm-launch-plugin
```

You can verify that the service is now running with:

```bash
service aesmd status
```

Finally, the current user must also be added to the aesm group:

```bash
sudo usermod -a -G aesmd $USER
```

2. To deploy the server using our Docker image you will first need to create an Intel Provisioning Certification Caching Service (PCCS) API key. This is necessary to be enable SGX attestation run-time workloads.

To do this, you'll need to:
- If you don't already have one, you'll need to create an account with [Intel](https://www.intel.com/content/www/us/en/homepage.html).
- Once you have an account, follow this [link](https://api.portal.trustedservices.intel.com/provisioning-certification) and make sure you are logged in.
- Select `subscribe` in the `Get PCK Certificate/s` section.
[image]
- On the following screen, select `Add subscription`
[image]
- This will lead you to a page detailing your subscription. To view your API key you can click on `Show` under `primary key`. This is the key you will need in order to deploy the Docker image.
[image]

2. Now you've got your PCCS API key, you can run the docker image with the following command:

[TODO: CHECK THIS COMMAND]
```bash
docker run -it \
-p 9223:9223 \
-p 9224:9224 \ 
mithrilsecuritysas/blindai-preview-server:latest [YOUR_PCCS_API_KEY_HERE]
```

>If you need to install Docker, you can follow [the official Docker installation instructions](https://docs.docker.com/engine/install). 

Once the server has been deployed, users can connect to your server by using the client PyPi package API and specifying the server IP address and ports when using the `connect` method.

>Note that by default the port opened in 9923 is running on http only. For production, we strongly recommend setting up a ***reverse-proxy*** that will manage and encrypt the traffic from the client to the blindAI server. Many free reverse-proxy implementations exist, such as **caddy**, **Nginx** and **Apache**:

- [https://caddyserver.com/docs/quick-starts/reverse-proxy](https://caddyserver.com/docs/quick-starts/reverse-proxy)
- [Nginx reverse proxy set-up guide](https://docs.nginx.com/nginx/admin-guide/web-server/reverse-proxy/)
- [Apache reverse proxy set-up guide](https://httpd.apache.org/docs/2.4/howto/reverse_proxy.html)

Once you have set up your reverse proxy to forward traffic to port 9923, clients should then modify the `unattested_server_port` option to the port on which you are running your reverse proxy when using the `connect` method to connect to the server.

If you do not set up a reverse proxy, users will need to set the `hazmat_http_on_untrusted_port` option to `True` when using blindai-preview's `connect()` function. Again, this is **not recommended** for production.

Once the server has been deployed, users can connect to your server by using the client PyPi package API and specifying the server IP address and ports when using the `connect` method.

### Building from source

If you want to **build from source**, perhaps because you want to contribute to the project or build from a certain branch or commit, you can find all the information you need to do so in our [building from source guide](../docs/advanced/build-from-sources/build-from-source.md)