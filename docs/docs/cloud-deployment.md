# Deployment on Azure DCsv3.

In order to run BlindAI using a VM, we need to make sure it has the right Intel SGX-ready hardware to run BlindAI. This is why you should use an [Azure DCsv3 VM](https://docs.microsoft.com/en-us/azure/virtual-machines/dcv3-series) as it has all the required pre-requisites for deploying BlindAI.

### Creating the VM

First thing first, you need to create an account on Azure. If you would like to try the service for free, you can get [a free trial.](https://azure.microsoft.com/en-us/free/) Follow the link for more information.

Once you have created your account and activated the free credits of $200, you can search for `Azure Confidential Computing` and then click on "Create".

![Confidential Computing VM](../assets/2022-02-24_11_09_07.png)

![Start the creation process.](../assets/2022-02-24_11_09_26.png)

After this, you will start to see a configuration screen. Please select either **Ubuntu 18.04 or 20.04. For security reasons, it is strongly advised to use a SSH public key in order to use the VM.**

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

Once you are online, we need to make sure that the SGX drivers are installed. You can do it very easily like this:&#x20;

![](../assets/2022-02-24_12_17_25.png)

[LAURA: NOTE TO SELF: UP TO HERE]

### Security
[TODO: EXPLAIN THE LINK WITH THE HAZMAT OPTION]

**The port opened in 9923 is considered as unsecure.** 

By default the port opened in 9923 is running on http only. For production, we strongly recommend setting up a ***reverse-proxy*** that will manage and encrypt the traffic from the client to the blindAI server. Many free reverse-proxy implementations exist, such as **caddy**, **Nginx** and **Apache**:

- [https://caddyserver.com/docs/quick-starts/reverse-proxy](https://caddyserver.com/docs/quick-starts/reverse-proxy)
- [Nginx reverse proxy set-up guide](https://docs.nginx.com/nginx/admin-guide/web-server/reverse-proxy/)
- [Apache reverse proxy set-up guide](https://httpd.apache.org/docs/2.4/howto/reverse_proxy.html)

### Deploying the server for production

Now that you are now connected to your Azure DCsv3 VM via SSH in VSCode. You can set-up BlindAI with the following steps:

1. The first step is to follow our [Azure DCsv3 set-up guide](https://github.com/mithril-security/blindai-preview/blob/main/docs/docs/cloud-deployment.md) for a step-by-step guide of how to set up your Azure DCsv3 VM.

2. Clone blindai github repo and submodules
- `git clone https://github.com/mithril-security/blindai-preview --recursive`

3. Open the `blindai-preview` folder in VSCode- make sure to do this in your VSCode window where you are connected to your VM by SSH.   

4. Replace the .devcontainer folder with the devcontainer-azure/.devcontainer folder. 
- `rm -rf .devcontainer`
- `mv devcontainer-azure/.devcontainer .devcontainer`

5. Select the `Dev Containers: Reopen in Container` option. [TODO: explain how]
This will create and open a Docker container for you to work in which will contain all the dependencies you need to run and use blindai-preview. This may take some time since there are several dependencies that must be installed.

6. You should now be within your dev container in VSCode. Open a new terminal and install the client:
- `cd client`
- `poetry install` 
- `poetry shell`

Congratulations, you are now ready to run our test programs or create your own scripts or notebooks!

You can now use our justfile to:
- Launch the server: `just run –release`
- Run our tests: `just test`

>Make sure you are in the root of the blindai-preview directory to make use of the justfile commands.

You can check out our [how-to using github repo instead of PyPI packages](link) to see an example of the full workflow using BlindAI.

=== "Hardware mode (Azure DCsv3 VMs)"

    To run the server on azure, and after installing all the dependencies needed :
    ```bash
    BLINDAI_AZURE_DCS3_PATCH=1 just release 
    # or 
    BLINDAI_AZURE_DCS3_PATCH=1 just run
    ```
