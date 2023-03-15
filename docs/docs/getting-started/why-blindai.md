# Why Blindai?
________________

AI solutions tend to be deployed in one of three ways: on the **Cloud**, **on-premise** or **on-device**. 

Cloud deployment offers users **ease-of-use** and a **wide offer of AI models** but it puts users' **data at risk**. Their privacy is left in the hands of the person or company who operates the service, the cloud operator, their sysadmins and other people who each need to be trusted. In general, this means that Cloud deployment is currently not suitable for users with sensitive data such as hospitals wanting to leverage patient data to improve healthcare.

Users with sensitive data may instead turn to on-premise or on-device deployment as a more privacy-friendly alternative to Cloud deployment, but this **increased privacy** comes at a **great cost** in terms of ease-of-use. 
- On-premise deployment requires on-site expertise that is not available to many companies.
- AI models storage space and power are limited by on-site hardware (on-premise deployement) or user devices (on-device deployment).
- AI models need to be embedded in the application distributed to the client, putting them at risk of being stolen in on-device solutions.

**BlindAI** offers the best of both worlds: the **ease-of-use** and **wide offer** of Cloud deployment with the **increased privacy** of on-premise and on-device solutions. We take advantage of the power of confidential computing, and more specifically Intel Software Guard Extension (**Intel SGX**), to enable user data to be processed remotely without the risk of unauthorized access or tampering.

## How does it work?

Intel processors with SGX can create **secure enclaves**. They are self-contained zones where the **processor guarantees** that software running inside **cannot be tampered with** by the host operating system, hypervisor, and even its BIOS. 

Users can upload their data and get their result via a **secure API** provided by the enclave. AI models are run on user data inside the enclave protecting both the user data from potential attacks and providing enhanced security for the AI models compared with on-premise alternatives.

To get introduced to how you can use BlindAI to keep your data safe, check out our [Quick Tour](#Quick tour)!