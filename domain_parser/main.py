import argparse

from dns_dump import dump_dns
from whois_info import get_whois_inf
#from search_certs import get_subdomains_in_cert
from get_ssl_inf import get_ssl_inf
from get_web_servs import get_web_servers
from admin_panel import start_adm_search


def get_args():
    args = argparse.ArgumentParser(description='DNS dumper')
    args.add_argument('-d', '--domain',  required=True, help='Target domain name')
    args = args.parse_args()

    return args


if __name__ == '__main__':
    args = get_args()
    domain  = args.domain
    
    print("***WHOIS INFO***")
    wh_inf = get_whois_inf(domain)
    for key, value in wh_inf.items():
        # if isinstance(value, list):
            # value = ', '.join(value)
        print(f"{key}: {value}")
    
    print("\n***DNS DUMP***")
    dump_dns(domain)
    
    # sert_inf = get_subdomains_in_cert(domain)
    # if sert_inf != None:
    #     print(sert_inf)


    ssl_inf = get_ssl_inf(domain)
    print("\n***SSL CERT INF***")
    for key, value in ssl_inf.items():
        print(f". {key}: {value}")

    web_servers = get_web_servers(domain)
    print("\n***WEB SERVERS***")
    for i in web_servers:
        print(". ", i)


    print("\n***ADMIN PANEL INF***")
    for i in start_adm_search(domain):
        print(".. ", i)
