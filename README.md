<a name="readme-top"></a>

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![Apache License][license-shield]][license-url]


<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/mithril-security/blindai">
    <img src="https://github.com/mithril-security/blindai/blob/master/assets/logo.png" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">BlindAI</h3>

[![Website][website-shield]][website-url]
[![Blog][blog-shield]][blog-url]
[![LinkedIn][linkedin-shield]][linkedin-url]

  <p align="center">
    <b>BlindAI</b> helps deploy AI models with an added <b>privacy layer</b>, 
    protecting the data sent to be analysed by the model and the model's IP. 
    <br />
    <a href="https://blindai.mithrilsecurity.io/en/latest/"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/mithril-security/blindai">Try Demo</a>
    ·
    <a href="https://github.com/mithril-security/blindai/issues">Report Bug</a>
    ·
    <a href="https://github.com/mithril-security/blindai/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#-about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#-getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#-usage">Usage</a></li>
    <li><a href="#-roadmap">Roadmap</a></li>
    <li><a href="#-getting-help">Getting Help</a></li>
    <li><a href="#-license">License</a></li>
    <li><a href="#-contact">Contact</a></li>
    <li><a href="#-disclaimer">Disclaimer</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## 🔒 About The Project

BlindAI is a **confidential AI inference server**. It works like any regular AI inference solution but **with an added privacy layer**. 

AI solutions tend to be deployed in one of two ways: on the Cloud or on-premise. Cloud deployment offers users ease-of-use and a wide offer of AI models but it puts users' data at risk. On-premise deployment is a secure alternative, but the increased privacy comes at a great cost in terms of ease-of-use. 

BlindAI aims to offer the best of both worlds: the **ease-of-use** and wide offer of Cloud deployment with the **security** of on-premise solutions. We take advantage of the power of confidential computing, and more specifically Intel Software Guard Extension (Intel SGX), to enable user data to be processed remotely without the risk of unauthorized access or tampering. The code running inside Intel SGX cannot be tampered with by the host operating system, hypervisor, and even its BIOS. 

>*You can learn more about Intel SGX, Trusted Execution Environements and how they work [in our documentation](LINK).*

Our solution comes in two parts:

- A secure inference **server** to deploy AI models with privacy guarantees 
- A Python **client** SDK to securely query the remote AI models


### Built With 

[![Rust][Rust]][Rust-url] [![Python][Python]][Python-url] [![Intel-SGX][Intel-SGX]][Intel-sgx-url] [![Tract][Tract]][tract-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->
## 🚀 Getting Started

### Finding the right deployment method for your use case

The first thing to establish is which of the following three cases you fall under:

### Case one: Testing BlindAI without hardware security guarantees

Pros:
- Quick and easy.
- Works on any device. Very few pre-requisites.
- Demos available on BlindAI Github.

Cons:
- This option does not offer the hardware security guarantees of Intel SGX. It is not suitable for production.


**recommended 🥇**
### Case two: Deploying BlindAI on Azure DCsv3 VM

Pros:
- Straight-forward deployment. Intel SGX is already installed on this VM.
- No requirement to have your own Intel SGX-ready device or a particular distribution. 
- Secure. Hardware security guarantees protect your data and model from any third-party access.

Cons:
- More expensive than local production.


### Case three: On-premise deployment

Pros:
- Secure. Hardware security guarantees protect your data and model from any third-party access.
- Can be less costly than paying for access to VM.

Cons:
- You must have an Intel SGX-ready device with `SGX+FLC` support.
- Depending on your specific requirements, we would usually only recommend this option if you have SGX2, which has a better performance and much more memory available. The physical protected memory for SGX1 is limited to 128mb.
- You need to install all the pre-requisites.

>How can I check if I have an Intel SGX-ready device with `SGX+FLC` support?

  ```
  git clone https://github.com/ayeks/SGX-hardware
  cd SGX-hardware
  gcc test-sgx.c -o test-sgx
  ./test-sgx | grep "sgx launch control"
  ```

- If your output is `sgx launch control: 1`, you have an Intel SGX-ready device with `SGX+FLC` support.
- If your output is `sgx launch control: 0`, you do not have an Intel SGX-ready device with `SGX+FLC` support.

>How can I check if I have SGX1 or SGX2?

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

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Installation

Now, that you have identified the right deployment mode for you, you can follow the installation instructions for your case.

### Case one: Testing BlindAI without hardware security guarantees

1. Check out our [quick tour notebook](link). This will show you how you can install and use BlindAI's client and server testing packages.
2. Feel free to test your own Python scripts or notebooks using the `blindai_preview` and `blindai_preview_server` PyPi packages.
If you have any trouble with these your test programs, compare your usage against our [example notebooks](link) or contact us via Discord or Github!

### Case two: Deploying BlindAI on Azure DCsv3 VM

Firstly, you'll need to check out the instructions for setting up your Azure DCsv3 VM [here](link)

Then, if you want to **deploy the server for production**, you can run our `on_premise_server_deployment.sh` script in your vm which will automate deployment for you.

If you want to **install the client and server for local development**, either because you want to contribute to the project or make your own local modifications to the code,
check out the instructions installing BlindAI for development on an-premise [here](link)

### Case three: On-premise deployment

If you just want to **deploy the server for production**, you can run our `on_premise_server_deployment.sh` script which will automate deployment for you.

`./on_premise_server_deployment.sh`

If you want to **install the client and server for local development**, either because you want to contribute to the project or make your own local modifications to the code,
check out the instructions installing BlindAI for development on an-premise [here](link)


<!-- USAGE EXAMPLES -->
## 🔆 Usage

You can go try out our [Quick tour](LIEN) in the documentation to discover BlindAI with a hands-on example using [COVID-Net](https://github.com/lindawangg/COVID-Net).

But here’s a taste of what using BlindAI could look like 🍒

PUT ONE EXAMPLE (ALSO SOME LINE FROM QUICK TOUR I GUESS)

_For more examples, please refer to the [Documentation](https://blindai.mithrilsecurity.io/en/latest/)_

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ROADMAP -->
## 🎯 Roadmap

WRITE DOWN THE FEATURES WE **ALREADY** IMPLEMENTED. NOTHING SATISFYING LIKE A LIST WITH CHECKED BOXES.

WE CAN ALSO RENAME THAT PART **KEY FEATURES**

- [ ] Feature 1
- [ ] Feature 2
- [ ] Feature 3
    - [ ] Nested Feature

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING HELP -->

## 🙋 Getting help

* Go to our [Discord](https://discord.com/invite/TxEHagpWd4) #support channel
* Report bugs by [opening an issue on our BlindAI GitHub](https://github.com/mithril-security/blindai/issues)
* [Book a meeting](https://calendly.com/contact-mithril-security/15mins?month=2023-03) with us

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- LICENSE -->
## 📜 License

Distributed under the Apache License, version 2.0. See [`LICENSE.md`](https://www.apache.org/licenses/LICENSE-2.0) for more information.


<!-- CONTACT -->
## 📇 Contact

Mithril Security - [@MithrilSecurity](https://twitter.com/MithrilSecurity) - contact@mithrilsecurity.io

Project Link: [https://github.com/mithril-security/blindai](https://github.com/mithril-security/blindai)


<!-- DISCLAIMER -->
## 📢 Disclaimer

IF WE NEED TO SAY STUFF ABOUT PRODUCTION READINESS OF BLINDAI

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://github.com/alexandresanlim/Badges4-README.md-Profile#-blog- -->
[contributors-shield]: https://img.shields.io/github/contributors/mithril-security/blindai.svg?style=for-the-badge
[contributors-url]: https://github.com/mithril-security/blindai/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/mithril-security/blindai.svg?style=for-the-badge
[forks-url]: https://github.com/mithril-security/blindai/network/members
[stars-shield]: https://img.shields.io/github/stars/mithril-security/blindai.svg?style=for-the-badge
[stars-url]: https://github.com/mithril-security/blindai/stargazers
[issues-shield]: https://img.shields.io/github/issues/mithril-security/blindai.svg?style=for-the-badge
[issues-url]: https://github.com/mithril-security/blindai/issues
[license-shield]: https://img.shields.io/github/license/mithril-security/blindai.svg?style=for-the-badge
[license-url]: https://github.com/mithril-security/blindai/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-Jobs-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/company/mithril-security-company/
[website-url]: https://www.mithrilsecurity.io
[website-shield]: https://img.shields.io/badge/website-000000?style=for-the-badge&colorB=555
[blog-url]: https://blog.mithrilsecurity.io/
[blog-shield]: https://img.shields.io/badge/Blog-000?style=for-the-badge&logo=ghost&logoColor=yellow&colorB=555
[product-screenshot]: images/screenshot.png
[Python]: https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue
[Python-url]: https://www.python.org/
[Rust]: https://img.shields.io/badge/rust-FFD43B?style=for-the-badge&logo=rust&logoColor=black
[Rust-url]: https://www.rust-lang.org/fr
[Intel-SGX]: https://img.shields.io/badge/SGX-FFD43B?style=for-the-badge&logo=intel&logoColor=black
[Intel-sgx-url]: https://www.intel.fr/content/www/fr/fr/architecture-and-technology/software-guard-extensions.html
[Tract]: https://img.shields.io/badge/Tract-FFD43B?style=for-the-badge
[tract-url]: https://github.com/mithril-security/tract/tree/6e4620659837eebeaba40ab3eeda67d33a99c7cf

<!-- Done using https://github.com/othneildrew/Best-README-Template -->
