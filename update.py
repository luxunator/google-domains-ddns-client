import requests
import socket
import pycurl
import json
from io import BytesIO


def main():
    config = get_config()
    new_ip = current_ip()  # Gets Current Public IP
    config_ip = ddns_ip(config['hostname'])  # Gets Config Hostname IP
    if new_ip == config_ip:
        with open('log.txt', 'a') as log:
            log.write(f'Update not needed as IP address is already set for this host with IP: {config_ip}\n')
    else:
        response = update(new_ip, config)
        log_response(response)


# Force Curl to get Public IPv4
def current_ip():
    buff = BytesIO()
    curl = pycurl.Curl()
    curl.setopt(curl.URL, "https://domains.google.com/checkip")
    curl.setopt(curl.IPRESOLVE, curl.IPRESOLVE_V4)
    curl.setopt(curl.WRITEDATA, buff)
    curl.perform()
    curl.close()
    rsp_ip = buff.getvalue().decode('iso-8859-1')
    return rsp_ip


def ddns_ip(hostname):
    ip = socket.gethostbyname(hostname)
    return ip


def get_config():
    with open('config.json') as config_file:
        config = json.load(config_file)
        return config


# Usage of Google DDNS API for update
def update(ip, config):
    config['myip'] = ip
    parameters = dict(list(config.items())[2:])
    r = requests.post(f"https://{config['username']}:{config['password']}@domains.google.com/nic/update", data=parameters)
    response = r.text
    return response


def log_response(response):

    response_switch = {
        'good': 'The update was successful with IP: ',
        'nochg': 'The supplied IP address is already set for this host with IP: ',
        'nohost': 'The hostname does not exist, or does not have Dynamic DNS enabled.',
        'badauth': 'The username / password combination is not valid for the specified host.',
        'notfqdn': 'The supplied hostname is not a valid fully-qualified domain name.',
        'badagent': 'Your Dynamic DNS client is making bad requests. Ensure the user agent is set in the request.',
        'abuse': 'Dynamic DNS access for the hostname has been blocked due to failure to interpret previous responses correctly.',
        '911': 'An error happened on our end. Wait 5 minutes and retry.',
        'conflict': 'Update conflicts with resource record of type '
    }

    # Parses Response to Format to Log
    response_desc = (response_switch.get(response, f'Invalid Response: {response}')
                     if len(response.split()) == 1 else
                     response_switch.get(response.split(' ')[0], f"Invalid Response: {response}") + response.split(' ')[1])

    with open('log.txt', 'a') as log:
        log.write(f'{response_desc}\n')


if __name__ == "__main__":
    main()
