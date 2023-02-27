import os
from setuptools import setup, find_packages
from setuptools.command.build_py import build_py
import pkg_resources
import re


def read(path):
    return open(os.path.join(os.path.dirname(__file__), path)).read()


DIR = os.path.dirname(__file__) or os.getcwd()
LONG_DESCRIPTION = read("README.md")
PKG_NAME = "blindai_preview_server"


def find_version():
    version_file = read(f"src/{PKG_NAME}/version.py")
    version_re = r"__version__ = \"(?P<version>.+)\""
    version = re.match(version_re, version_file).group("version")
    return version


class BuildPackage(build_py):
    def run(self):
        super(BuildPackage, self).run()


setup(
    name=PKG_NAME,
    version=find_version(),
    description="Server for BlindAI",
    long_description_content_type="text/markdown",
    keywords="confidential computing inference ai client enclave intel-sgx machine learning",
    cmdclass={"build_py": BuildPackage},
    long_description=LONG_DESCRIPTION,
    author="Mithril Security",
    author_email="contact@mithrilsecurity.io",
    classifiers=["Programming Language :: Python :: 3"]
)
