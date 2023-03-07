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
    <br />
    protecting both the data sent to be analysed by the model and the model's IP. 
    <br />
    <a href="https://blindai.mithrilsecurity.io/en/latest/"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/mithril-security/blindai">View Demo</a>
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
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#disclaimer">Disclaimer</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

BlindAI is a **confidential AI inference server**. It works like any regular AI inference solutions by helping AI engineers serve models for end-users to benefit from their predictions, but **with an added privacy layer**. 

Data sent by users to the AI model is kept confidential at all times, from the transfer to the analysis. This way, users can benefit from AI models without ever having to expose their data in clear to anyone: neither the AI service provider, nor the Cloud provider (if any), can see the data.

Confidentiality is assured by using special hardware-enforced Trusted Execution Environments. To read more about those, read our blog series [here](https://blog.mithrilsecurity.io/confidential-computing-explained-part-1-introduction/).

Our solution comes in two parts:

- A **secure inference server** to deploy AI models with privacy guarantees
- A **Python client SDK** to securely consume the remote AI models

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

* [![Rust][Rust]][Rust-url]
* [![Python][Python]][Python-url]
* [![Intel-SGX][Intel-SGX]][Intel-sgx-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

### Prerequisites

This is an example of how to list things you need to use the software and how to install them.
* npm
  ```sh
  npm install npm@latest -g
  ```

### Installation

1. Clone the repo with the submodules
   ```sh
   git clone --recursive git@github.com:mithril-security/blindai-preview.git 
   ```
2. If you are in an Azure machine <br>
   Replace the `.devcontainer` folder by the `devcontainer-azure/.devcontainer` folder. Open it in your code editor and reopen in Container.
3. At the root of the project, create a virtual environment and install the Client SDK
   ```sh
   cd client
   poetry install
   poetry shell
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources.

_For more examples, please refer to the [Documentation](https://example.com)_

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [ ] Feature 1
- [ ] Feature 2
- [ ] Feature 3
    - [ ] Nested Feature

See the [open issues](https://github.com/mithril-security/blindai/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Mithril Security - [@MithrilSecurity](https://twitter.com/MithrilSecurity) - contact@mithrilsecurity.io

Project Link: [https://github.com/mithril-security/blindai](https://github.com/mithril-security/blindai)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- DISCLAIMER -->
## Disclaimer

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
[Rust]: https://img.shields.io/badge/rust-000000?style=for-the-badge&logo=rust&logoColor=white
[Rust-url]: https://www.rust-lang.org/fr
[Intel-SGX]: https://img.shields.io/badge/SGX-000000?style=for-the-badge&logo=intel&logoColor=white
[Intel-sgx-url]: https://www.intel.fr/content/www/fr/fr/architecture-and-technology/software-guard-extensions.html

<!-- Done using https://github.com/othneildrew/Best-README-Template -->
