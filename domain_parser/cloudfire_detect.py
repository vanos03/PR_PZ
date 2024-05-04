import socket
from ipaddress import ip_network, ip_address

import requests

cldfire_url = 'https://www.cloudflare.com/ips-v4'

def ip_in_range(ip, addr):
    if ip_address(ip) in ip_network(addr):
        return True
    else:
        return False

def get_domain_ip(domain):
    try:
        return socket.gethostbyname(domain)
    except socket.gaierror:
        return None


    
def cloudfire_detect(domain):
    list_addr = []
    req = requests.get(cldfire_url).text.split('\n')

    for addr in req:
        list_addr.append(addr)

    ip = get_domain_ip(domain)
    if ip == None:
        return
    
    for addr in list_addr:
        detect = ip_in_range(ip, addr)
        if detect:
            return True
    
    return False

def search_domain_in_cloudfire(domain):
    url = f'https://crimeflare.herokuapp.com/?url={domain}'
    try:
        req = requests.get(url).text.split("</pre>")[0].split('Real IP:')[1].strip().split()[1]
        return req
    except IndexError:
        return False


