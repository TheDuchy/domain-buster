#Written by Jan "Duchy" Neduchal 2019
#This code is under the IDFC Licence.
#The IDFC License means do whatever you want just give credit
import requests
import argparse
import sys
import re
import socket
from sty import fg, rs


def isIP(domain):
    ips = re.findall(r"^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])", domain)
    if len(ips) == 0:
        return 0
    else:
        return 1


def scanForDomains(args, path):
    found = 0
    try:
        r = requests.get(path, timeout=args.timeout)
    except requests.exceptions.Timeout:
        sys.exit("Domain times out, maybe try to increase -t")
    domains = re.findall(r".https?:\/\/([^/|\"|\'|\#|\)]*)", r.text)
    for i in domains:
        if len(i) == 0:
            continue
        if isIP(i):
            print(fg(72,251,0) + "FOUND IP: " + fg.rs + i)
            found += 1
            continue
        try:
            socket.gethostbyname(i)
        except socket.gaierror:
            print(fg(72,251,0) + "COULD NOT RESOLVE DNS: " + fg.rs + i)
            found += 1
        except:
            pass
    #print(domains)
    if found == 0:
        print(fg(72,251,0) + "Didn't find any usefull stuff :(" + fg.rs)
if __name__ == "__main__":

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
    except requests.exceptions.ConnectionError:
        sys.exit("Server failed to respond, this is not a timeout")
    except:
        print(domain)
        sys.exit("A major fuckup happened, please submit an issue on github")

    scanForDomains(args, domain)
