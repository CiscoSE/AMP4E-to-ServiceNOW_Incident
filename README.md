# AMP4E-to-ServiceNOW_Incident

*This code utilizes the API capabilities from Cisco AMP for Endpoints to create ServiceNOW incidents*

---

**ToDo's:**

- [✓] Consider writing your README first.  Doing so helps you clarify your intent, focuses your project, and it is much more fun to write documentation at the beginning of a project than at the end of one, see:
    - [Readme Driven Development](http://tom.preston-werner.com/2010/08/23/readme-driven-development.html)
    - [GitHub Guides: Mastering Markdown](https://guides.github.com/features/mastering-markdown/)
- [✓] Ensure you put the [license and copyright header](./HEADER) at the top of all your source code files.
- [✓] Be mindful of the third-party materials you use and ensure you follow Cisco's policies for creating and sharing Cisco Sample Code.

---

## Motivation

Working at various companies, ServiceNOW has been the ITSM tool of choice and often times, engineers and managers want some integration between various systems and tools into this platform. So the motivation for this project is to provide an example of what can be accomplished with Cisco's platforms and other platforms.

## Before you use
Before you begin you need to ensure that you have the following:
* Cisco AMP for Endpoints installed and have a valid account
* ServiceNOW Account
* Optional: AWS Account

Make sure you modify the keys, user/pass and URL to match your various accounts.

AMP
* client_id<br/>
* api_key<br/>

ServiceNOW
* user<br/>
* pwd<br/>
* https://\<YOUR TENANT ACCOUNT\>.service-now.com/api/now/table/incident<br/>

## Features

- Go through all the AMP connectors installed in your environment and collect events that have a Malicious disposition and create an Incident for them into ServiceNOW.
- Optional: Easily run this out of AWS Lambda with high cost optimization.

## Technologies & Frameworks Used

The technologies used are Cisco's AMP for Endpoints, ServiceNOW for ITSM and optionally AWS Lambda to run the code in the cloud if desired.

**Cisco Products & Services:**

- Cisco AMP for Endpoints

**Third-Party Products & Services:**

- ServiceNOW (any current version)
- AWS Lambda (You will need an AWS account if you choose this route)

**Tools & Frameworks:**

- chalice

## Usage

Command line on your own workload.
```
$ python3 amp4e-servicenow-incident.py   # Install the required packages that this project uses.
```
On AWS Lambda executing every 120 seconds. (Optional)
```
$ virtualenv venv
$ source venv/bin/activate
$ pip3 install chalice
$ pip3 install requests
$ chalice new-project lambda-AMP4E-ServiceNOW
$ cd lambda-AMP4E-ServiceNOW
## Replace the app.py file with the one in this git repo under the chalice directory. Also remember to put your own data in.
$ chalice deploy
## To remove run chalice delete
```

## Installation Prerequisites
Python
```
$ pip3 install -r requirements.txt
```

AWS Lambda (Optional)
```
$ pip3 install chalice  # Install Chalice Framework to quickly create an AWS Lambda serverless workload. (Optional)
$ brew install awscli   # Install AWS CLI. (Optional)
$ aws configure         # AWS API keys setup. (Optional)
```

## Screenshot example
![alt text](https://github.com/CiscoSE/AMP4E-to-ServiceNOW_Incident/blob/master/images/Screen%20Shot%202019-01-03%20at%2011.28.05%20PM.png)

## Extending the code
You can also extend this code to load into the CMDB module, so that IT personnel can better capture user data, etc. There is a lot of flexibility and below is an example for Linux Servers (So imagine you installed AMP on your Linux servers).
```
$ curl -u 'admin':'password' -X GET https://dev123456.service-now.com/api/now/table/cmdb_ci_linux_server
```
## Authors & Maintainers

- George Seeto

## Credits
Credit to Cisco Dev-NET and the folks who hosted the Dev-NET workshop I was able to attend in December, 2018. In addition ServiceNOW inspiration comes from various companies I have come from where ServiceNOW was the main ITSM application of choice. 

## License

This project is licensed to you under the terms of the [Cisco Sample
Code License](./LICENSE).
