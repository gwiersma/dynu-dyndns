import public_ip as ip
import requests
import time
import argparse


RERUN = True

def create_header(API_KEY):
    """
    Creates a http header with content type
    """
    header = {'accept': 'application/json', 'API-Key': API_KEY, 'Content-Type': 'application/json'}
    return header


def checkIPchange(API_URL, DOMAIN_URL, AUTH_HEADER):
    current_ip = ip.get()

    output = requests.get(API_URL, headers=AUTH_HEADER)
    json_output = output.json()['domains']
    
    
    for id in json_output:
        if id['name'] == DOMAIN_URL:
            if id['ipv4Address'] != current_ip:
                print("IP changed from. Changing IP adress")

                DOMAIN_ID = id['id']
                POST_URL = API_URL + '/' + str(DOMAIN_ID)
                POST_BODY = {
                    "name": id['name'],
                    "group": id['group'],
                    "ipv4Address": current_ip,
                    "ipv6Address": '',
                    "ttl": id['ttl'],
                    "ipv4": id['ipv4'],
                    "ipv6": id['ipv6'],
                    "ipv4WildcardAlias": id['ipv4WildcardAlias'],
                    "ipv6WildcardAlias": id['ipv6WildcardAlias'],
                    "allowZoneTransfer": 'false',
                    "dnssec": 'false'
                }

                output = requests.post(POST_URL, headers=AUTH_HEADER, json=POST_BODY)

                if output.status_code == 200:
                    return True
                else:
                    return False
            else:
                pass
        else:
            pass

parser = argparse.ArgumentParser(
                    prog='Dynu Auto IP updater',
                    description='Program updates WAN IP for specific domain when changed',
                    epilog='Works with DYNU only')

parser.add_argument("-s", "--server",
                    help="API server URL",
                    required=True)
parser.add_argument("-t", "--token",
                    help="API token",
                    required=True)
parser.add_argument("-d", "--domain",
                    help="Domain URL",
                    required=True)
args = vars(parser.parse_args())

API_URL = args['server']
API_KEY = args['token']
DOMAIN_URL = args['domain']

while RERUN:
    HEADER = create_header(API_KEY)
    checkIPchange(API_URL, DOMAIN_URL, HEADER)
    time.sleep(120)

