# google-domains-ddns-client
Google Domains DDNS Client written in Python that automates updates by using the Google Domains DDNS API and Crontabs

## Installation
```bash
$ git clone https://github.com/luxunator/google-domains-ddns-client
$ cd google-domains-ddns-client/
$ pip install requirements.txt
```
## Usage
To start a DDNS Client task run the setup:
```bash
$ python setup.py
```
## Removal
As the client uses crontabs to update hourly you can manually remove all jobs or remove single job by running the setup:
```bash
$ crontab -r
# or
$ python setup.py
```
