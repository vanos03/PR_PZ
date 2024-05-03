import argparse
import dns.resolver
import sys

domains = ['google.com']
dns_servers = ['8.8.8.8', '8.8.4.4']
dns_resolve = dns.resolver.Resolver()
dns_resolve.nameservers = dns_servers
dns_rec_types = ['A', 'AAAA', 'AFSDB', 'APL', 'CAA', 'CDNSKEY', 'CDS', 'CERT',
                 'CNAME', 'DHCID', 'DLV', 'DNAME', 'DNSKEY', 'DS', 'HIP', 'IPSECKEY', 
                 'KEY', 'KX', 'LOC', 'MX', 'NAPTR', 'NS', 'NSEC', 'NSEC3', 'NSEC3PARAM', 
                 'OPENPGPKEY', 'PTR', 'RRSIG', 'RP', 'SIG', 'SMIMEA', 'SOA', 'SRV', 'SSHFP', 
                 'TA', 'TKEY', 'TLSA', 'TSIG', 'TXT', 'URI']



def get_args():
    args = argparse.ArgumentParser(description='DNS dumper')
    args.add_argument('-d', '--domain',  required=True, help='Target domain name')
    args = args.parse_args()

    return args

def create_dns_rec(domain, type):
    try:
        answ = dns_resolve.query(domain, type)
        print(type, ' :', list(map(lambda a: a.address if type in ['A', 'AAAA'] else \
                a, answ)))
        return list(map(lambda a: a.address if type in ['A', 'AAAA'] else \
                a, answ))

    except dns.resolver.NXDOMAIN:
        print(f'Invalid domain: {domain}')
        sys.exit(1)
    except Exception as e:
        if isinstance(e, dns.resolver.NoAnswer):
            print(f'check {type}: No answer')


def dump_dns(domains):
    
    for domain in domains:
        print('domain: ', domain)
        for type in dns_rec_types:
            create_dns_rec(domain, type)


if __name__ == '__main__':
     dump_dns(domains)
    # args = get_args()
    # dns_resolve = dns.resolver.Resolver()
    # dns_resolve.nameservers = dns_servers
    # dns_answ = dns_resolve.resolve(domain)
    