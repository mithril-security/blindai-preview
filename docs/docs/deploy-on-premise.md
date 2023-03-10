# On-premise deployment

### Eligibility check

In order to deploy BlindAI on-premise, you will need an Intel SGX-ready device with `SGX+FLC` support.

You can check this with the following code:

  ```
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

```
git clone https://github.com/ayeks/SGX-hardware
cd SGX-hardware
gcc test-sgx.c -o test-sgx
./test-sgx | grep "sgx 1 supported"
```

- If your output is `sgx 1 supported: 1`, you have SGX1.
- If your output is `sgx 1 supported: 0`, you do not have SGX1.

```
./test-sgx | grep "sgx 2 supported"
```

- If your output is `sgx 2 supported: 1`, you have SGX2.
- If your output is `sgx 2 supported: 0`, you do not have SGX2.

### Intel SGX drivers

>Note that these instructions were created for Linux ubuntu 20.04-22.04 users.

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

### Server deployment only

1. Clone blindai github repo and submodules.
    ```git clone https://github.com/mithril-security/blindai-preview --recursive
    cd blindai-preview
    ```
2. We have made a script that will download everything you need and launch the server. You can run it to deploy the server by running:
    ```./on_premise_server_deployment.sh

    ```
This script will:
- Ensure you have docker installed.
- Set up the PCCS needed for attestation.
- Install and run the AESM service which allows our host machine to communicate with the enclave.
- Run the server in release mode
- [NOTE FOR ANDRE, CAN WE ALSO ADD THE REVERSE PROXY SETUP TO THIS SCRIPT OR MAKE AN ADDITIONAL SCRIPT?]

Once the server has been deployed, users can connect to your server by using the client PyPi package API and specifying the server IP address and ports when using the `connect` method.

>Note that by default the port opened in 9923 is running on http only. For production, we strongly recommend setting up a ***reverse-proxy*** that will manage and encrypt the traffic from the client to the blindAI server. Many free reverse-proxy implementations exist, such as **Nginx** and **Apache**:

- [Nginx reverse proxy set-up guide](https://docs.nginx.com/nginx/admin-guide/web-server/reverse-proxy/)
- [Apache reverse proxy set-up guide](https://httpd.apache.org/docs/2.4/howto/reverse_proxy.html)

>Note that if you make any changes to the server code before deploying the server, you will need to generate a new manifest.toml file and share it with any users accessing the server using the client API. The default manifest.toml file is generated at the root of the repo when the enclave is built. The manifest.toml files are used during the verification step of the connection progress to check that the server is not running any unexpected and potentially malicious code. You can learn more about this verification process [here](link).

### Installation for development

If you want to **install the client and server for local development**, either because you want to contribute to the project or make your own local modifications to the code, you can launch our development environment with the following steps:

1. Clone blindai github repo and submodules.
    ```git clone https://github.com/mithril-security/blindai-preview --recursive
    cd blindai-preview
    ```

2. Make sure you have docker installed on your machine. 
- If you need to install Docker, you can follow [the official Docker installation instructions](https://docs.docker.com/engine/install). 

You also need to make sure you haver the correct permissions to run docker commands without `sudo`. 
To check this, try running `docker run hello-world`. If this works, you can skip straight to the next step. If it doesn't, you need to add yourself to docker group: 
    ```
    sudo usermod -aG docker $USER && newgrp docker
    ```

3. Open the `blindai-preview` folder in VSCode.   

4. Make sure you have the remote container VSCode extension installed. If you don't, install this from the VSCode extensions marketplace.

5. Open the green menu at the bottom-left of the Visual Studio Code.
Choose: "Dev Containers: Reopen in Container".

This will create and open a Docker container for you to work in which will contain all the dependencies you need to run and use blindai-preview. This may take some time since there are several dependencies that must be installed.

You should now be within your dev container in VSCode. You can now make any changes you want to the client and server code.

### Compiling client and launching server

To compile the client once you have made changed to the client code:
    ```cd client
    poetry install
    poetry shell
    ```

You can also use the `justfile` to:
- Launch the server: 
    ```just run
    ```
- Run our tests:
    ```just test
    ```
>Make sure you are in the root of the blindai-preview directory to make use of the justfile commands.

You are now ready to run our test programs or create your own scripts or notebooks!

### Testing client and server modifications in a test program

If you want to run a script or notebook using the client after making changes to the source files replace `pip install blindai-preview` with `pip install [path/to/client/folder]`.

If you want to run a script or notebook using the server after making changes to the server, you can launch the server using `just run`. You can then connect to the server using the client API in your scripts/ test programs.

>Note that if you make any changes to the server code before deploying the server, you will need to generate a new manifest.toml file and share it with any users accessing the server using the client API. The default manifest.toml file is generated at the root of the repo when the enclave is built. The manifest.toml files are used during the verification step of the connection progress to check that the server is not running any unexpected and potentially malicious code. You can learn more about this verification process [here](link).

>Note that by default the port opened in 9923 is running on http only. For production, we strongly recommend setting up a ***reverse-proxy*** that will manage and encrypt the traffic from the client to the blindAI server. Many free reverse-proxy implementations exist, such as **Nginx** and **Apache**:

- [Nginx reverse proxy set-up guide](https://docs.nginx.com/nginx/admin-guide/web-server/reverse-proxy/)
- [Apache reverse proxy set-up guide](https://httpd.apache.org/docs/2.4/howto/reverse_proxy.html)

### Examples

You can check out our [how-to using github repo instead of PyPI packages](link) to see an example of the full workflow using BlindAI.