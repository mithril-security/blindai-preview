# Deployment on Azure DCsv3.

In order to run BlindAI using a VM, we need to make sure it has the right Intel SGX-ready hardware to run BlindAI. This is why we strongly recommend setting up an [Azure DCsv3 VM](https://docs.microsoft.com/en-us/azure/virtual-machines/dcv3-series) as it has all the required pre-requisites for deploying BlindAI. The following installation guide has been created for Azure DCsv3 VMs.

### Creating the VM

First thing first, you need to create an account on Azure. If you would like to try the service for free, you can get [a free trial.](https://azure.microsoft.com/en-us/free/) Follow the link for more information.

Once you have created your account and activated the free credits of $200, search for `Azure Confidential Computing` and click on "Create".

![Confidential Computing VM](../assets/2022-02-24_11_09_07.png)

![Start the creation process.](../assets/2022-02-24_11_09_26.png)

After this, you will see a configuration screen. Please select either **Ubuntu 18.04 or 20.04. For security reasons, it is strongly advised to use a SSH public key in order to use the VM.**

![Basic configuration](../assets/2022-02-24_11_57_19.png)

On the next page, you will choose the VM you want to use. We strongly advise you to pick the **DC2s v3 VM** to test BlindAI. Before going to the next page, please remember to **allow the connection from SSH**.

![VM settings](../assets/2022-02-24_11_12_12.png)

![Choose a VM](../assets/2022-02-24_11_10_26.png)

After this screen, please validate and create the VM.

![Validate and create the VM.](../assets/2022-03-02_16_41_19.png)

After a few minutes, the VM will be successfully deployed. Before connecting to the VM, **it is strongly advised to set up a DNS name, in order to simplify the connection as much as possible.**

![Setting up DNS name - 1](../assets/2022-03-02_16_38_31.png)

![Setting up DNS name - 2](../assets/2022-02-24_12_07_22.png)

Once you are done with this, we have to **open the ports used by BlindAI.** You need to open the BlindAI default ports **9923 and 9924.**

![](../assets/image.png)

![](../assets/image_1.png)

### Using the VM

You can now start the VM. In order to have a good user experience, we recommend you download [**Visual Studio Code**](https://code.visualstudio.com/) and get the extension [**Remote - SSH**](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-ssh). 

Setting up a SSH connection is fairly easy in Visual Studio Code. All you need to do is add a SSH Host (you can find this option in **the Command Palette**):&#x20;

![](../assets/2022-02-24_12_15_41.png)

![The DNS name comes in handy here as you won't need to update the host after the first configuration.](../assets/2022-02-24_12_15_35.png)

After that, you need to select "Connect to Host" in **the Command Palette** and select your DNS name.

![](../assets/2022-02-24_12_53_38.png)

### Server deployment only

Once you are connected to the VM. You can do the following steps to deploy the server:

1. Clone blindai github repo and submodules.
    ```git clone https://github.com/mithril-security/blindai-preview --recursive
    cd blindai-preview
    ```

2. We have made a script for server deployment:
    ```./vm_server_deployment.sh

    ```
This script will:
- Ensure you have all necessary pre-requisites
- Run the server in release mode
- [NOTE FOR ANDRE: CAN WE ALSO ADD THE REVERSE PROXY SETUP TO THIS SCRIPT OR MAKE AN ADDITIONAL SCRIPT?
NOTE FOR ANDRE: SHOULD WE MAKE DIFFERENT OPTIONS FOR RELEASE MODE VS LOCAL MODE OR SOMETHING?]

Once the server has been deployed, users can connect to your server by using the client PyPi package API and specifying the server IP address and ports when using the `connect` method.

>Note that by default the port opened in 9923 is running on http only. For production, we strongly recommend setting up a ***reverse-proxy*** that will manage and encrypt the traffic from the client to the blindAI server. Many free reverse-proxy implementations exist, such as **caddy**, **Nginx** and **Apache**:

- [https://caddyserver.com/docs/quick-starts/reverse-proxy](https://caddyserver.com/docs/quick-starts/reverse-proxy)
- [Nginx reverse proxy set-up guide](https://docs.nginx.com/nginx/admin-guide/web-server/reverse-proxy/)
- [Apache reverse proxy set-up guide](https://httpd.apache.org/docs/2.4/howto/reverse_proxy.html)

If you do not set up a reverse proxy, users will need to set the `hazmat_http_on_untrusted_port` option to `True` when using blindai-preview's `connect()` function. Again, this is **not recommended** for production.

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

4. Open the green menu at the bottom-left of the Visual Studio Code.
Choose: "Dev Containers: Reopen in Container".

This will create and open a Docker container for you to work in which will contain all the dependencies you need to run and use blindai-preview. This may take some time since there are several dependencies that must be installed.

You should now be within your dev container in VSCode. You can now make any changes you want to the client and server code.

### Compiling client and launching server

To compile the client once you have made changed to the client code:
    ```cd client
    poetry install
    poetry shell
    ```

You can use the `justfile` to:
- Launch the server: 
    ```just run
    ```
- Run our tests:
    ```just test
    ```
>Make sure you are in the root of the blindai-preview directory to make use of the justfile commands.

>Note that if you make any changes to the server code before deploying the server, you will need to generate a new manifest.toml file and share it with any users accessing the server using the client API. The default manifest.toml file is generated at the root of the repo when the enclave is built. The manifest.toml files are used during the verification step of the connection progress to check that the server is not running any unexpected and potentially malicious code. You can learn more about this verification process [here](link).

You are now ready to run our test programs or create your own scripts or notebooks!

### Testing client and server modifications in a test program

If you want to run a script or notebook using the client after making changes to the source files replace `pip install blindai-preview` with `pip install [path/to/client/folder]`.

If you want to run a script or notebook using the server after making changes to the server, you can launch the server using `just run`. You can then connect to the server using the client API in your scripts/ test programs.

>Note that by default the port opened in 9923 is running on http only. For production, we strongly recommend setting up a ***reverse-proxy*** that will manage and encrypt the traffic from the client to the blindAI server. Many free reverse-proxy implementations exist, such as **caddy**, **Nginx** and **Apache**:

- [https://caddyserver.com/docs/quick-starts/reverse-proxy](https://caddyserver.com/docs/quick-starts/reverse-proxy)
- [Nginx reverse proxy set-up guide](https://docs.nginx.com/nginx/admin-guide/web-server/reverse-proxy/)
- [Apache reverse proxy set-up guide](https://httpd.apache.org/docs/2.4/howto/reverse_proxy.html)

If you do not set up a reverse proxy, users will need to set the `hazmat_http_on_untrusted_port` option to `True` when using blindai-preview's `connect()` function. Again, this is **not recommended** for production.

### Examples

You can check out our [how-to using github repo instead of PyPI packages](link) to see an example of the full workflow using BlindAI.