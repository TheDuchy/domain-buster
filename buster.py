#Written by Jan "Duchy" Neduchal 2019
#This code is under the IDFC Licence.
#The IDFC License means do whatever you want just give credit
import requests
import argparse
import sys
import re
import socket

parser = argparse.ArgumentParser(description='Simple tool for domain busting')

parser.add_argument('-d', '--domain', help='Target domain / file' ,required=True)
parser.add_argument('-t', '--timeout', default=2, type=int, help='Timeout treshold, default is "2" sec')
parser.add_argument('-o', '--output', default='result.txt', help='Name for the file output. Default is "result.txt"')

args = parser.parse_args()
if not re.findall(r"^https?://", args.domain):
    domain = "http://" + args.domain
else:
    domain = args.domain

try:
    r = requests.get(domain, timeout=args.timeout)
    if r.status_code == 404:
        sys.exit("Domain returns HTTP 404")
except requests.exceptions.Timeout:
    sys.exit("Domain times out, maybe try to increase -t")
except:
    print(domain)
    sys.exit("A major fuckup happened, please submit an issue on github")


def scanForDomains(path):
    try:
        r = requests.get(path, timeout=args.timeout)
    except requests.exceptions.Timeout:
        sys.exit("Domain times out, maybe try to increase -t")
    domains = re.findall(r".https?:\/\/([^/|\"|\'|\#|\)]*)", r.text)
    for i in domains:
        if len(i) == 0:
            continue
        try:
            socket.gethostbyname(i)
        except socket.gaierror:
            print("COULD NOT RESOLVE DNS: " + i)
        except:
            pass
    #print(domains)
if __name__ == "__main__":
    scanForDomains(domain)
