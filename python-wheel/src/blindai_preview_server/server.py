import subprocess
import urllib.request
import zipfile
import io
import os
from .version import __version__ as app_version
from urllib.error import HTTPError
from os import path
from subprocess import Popen


class BlindAIServer:
    """Popen object wrapper
    Args:
        process (Popen): Process object returned by subprocess.popen
    """

    def __init__(self, process):
        self.process = process

    def getProcess(self):
        return self.process


class NotFoundError(Exception):
    """This exception is raised when there was an error opening an URL.
    Args:
        Args:
        message (str): Error message.
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    pass


def extract_zip(data):
    with zipfile.ZipFile(io.BytesIO(data)) as zip:
        zip.extractall("./")


def handle_download(path_str: str, url: str, name: str, error_msg: str):
    if path.exists(path_str) is False:
        print("Downloading {}...".format(name))
        try:
            response = urllib.request.urlopen(url)
            extract_zip(response.read())
        except HTTPError as e:
            raise NotFoundError(
                "{}. Exact error code: {}".format(error_msg, e.code)
            ) from None
    else:
        print("{} already installed".format(name))


def start_server(blindai_path: str) -> BlindAIServer:
    os.chmod(blindai_path, 0o755)
    os.chdir(os.getcwd() + "/bin")
    process = subprocess.Popen([blindai_path], env=os.environ)
    os.chdir("..")
    print("BlindAI server is now running on port 9924 & 9923")
    srv = BlindAIServer(process)
    return srv


def stop(srv: BlindAIServer) -> bool:
    """Stop BlindAI server.
    This method will kill the running server, if the provided BlindAIServer object is valid.
    Args:
        srv (BlindAIServer): The running process of the server.
    Return:
        bool, determines if the process was successful or not.
    Raises:
        None
    """

    if (
        srv is not None
        and srv.getProcess() is not None
        and srv.getProcess().poll() is None
    ):
        print("Stopping BlindAI's server...")
        srv.getProcess().kill()
        return True
    else:
        print("BlindAI's server already stopped")
        return False


def start() -> BlindAIServer:
    """Start BlindAI server.
    The method will download BlindAI Preview's server binary.
    The server will then run, as a subprocess, allowing to run the rest of your Google Colab/Jupyter Notebook environment.
    Args:
        None
    Return:
        BlindAIServer object, the process of the running server.
    Raises:
        NotFoundError: Will be raised if one of the URL the wheel will try to access is invalid. This might mean that either there is no available binary of BlindAI's server.
        Other exceptions might be raised by zipfile or urllib.request.
    """
    bastionlab_path = os.getcwd() + "/bin/blindai_server"
    bastion_url = f"https://github.com/mithril-security/blindai-preview/releases/download/v{app_version}/blindai-{app_version}-linux.zip"
    handle_download(
        bastionlab_path,
        bastion_url,
        f"BlindAI server (version {app_version})",
        "The release might not be available yet for the current version",
    )
    process = start_server(bastionlab_path)
    return process
