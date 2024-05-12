import argparse
import time

from nmap_scan import nmap_A_scan
from find_subdomains import find_subdomains
from dns_dump import dump_dns
from nist_nvd_req import cve_search


def get_args():
    args = argparse.ArgumentParser(description='DNS dumper')
    args.add_argument('-d', '--domain',  required=True, help='Target domain name')
    args = args.parse_args()

    return args


if __name__ == '__main__':
    start_time = time.time()
    args = get_args()
    domain  = args.domain

    try:
        subdomains = find_subdomains(domain)
        subdomains += dump_dns(domain)
        subdomain = set(subdomains)
        print("-"*10 + f"{domain} subdomains:" + "-"*10, '\n', subdomains)
        cpe = set()
        for subdomain in subdomains:
            cpe_tmp = set()
            subdomain = str(subdomain).replace('www.', '')
            print(f"\n---  Search CPE for {subdomain} --- ")
            cpe_tmp = nmap_A_scan(subdomain)
            if cpe_tmp != ['']:
                print("...   CPE: ", cpe_tmp)
            else:
                print("...   CPE: ", "none")
            for i in cpe_tmp:
                if cpe != '' or cpe != None:
                    cpe.add(i)
        print(cpe)
        # cpe = {'', 'cpe:/a:pureftpd:pure-ftpd', 'cpe:/a:igor_sysoev:nginx', 
        # 'cpe:/a:php:php:7.2.29', 'cpe:/a:igor_sysoev:nginx:1.22.11.22.1'}
        for i in cpe:
            if i != None and i != '':
                print('\n' + "-"*10 + "Check CPE: " + i  +"-"*10)
                cve = cve_search(i.replace("cpe:/", ''))
                if cve["CVE"] != []:
                    print('\n' + '-'*10 + "Potential CVE" + '-'*10)
                    for i in cve["CVE"]:
                        print('.. ' + i.replace("'", ""))
                else:
                    print("...   none")
                if cve["CVSS"] != []:
                    print('\n' + '-'*10 + "CVSS" + '-'*10)
                    # print("\nCVSS: ", )
                    for i in cve["CVSS"]:
                        print('.. ' + i.replace("'", ""))
                else:
                    print("...   none")
        print("\n Time: " + str(round((time.time()-start_time) / 60)) + " min")
    except:
        pass

