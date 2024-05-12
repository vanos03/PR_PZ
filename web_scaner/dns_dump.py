
import dns.resolver
import sys


# domains = ['google.com']
dns_servers = ['8.8.8.8', '8.8.4.4']
dns_resolve = dns.resolver.Resolver()
dns_resolve.nameservers = dns_servers
dns_rec_types = ['A', 'AAAA', 'AFSDB', 'APL', 'CAA', 'CDNSKEY', 'CDS', 'CERT',
                 'CNAME', 'DHCID', 'DLV', 'DNAME', 'DNSKEY', 'DS', 'HIP', 'IPSECKEY', 
                 'KEY', 'KX', 'LOC', 'MX', 'NAPTR', 'NS', 'NSEC', 'NSEC3', 'NSEC3PARAM', 
                 'OPENPGPKEY', 'PTR', 'RRSIG', 'RP', 'SIG', 'SMIMEA', 'SOA', 'SRV', 'SSHFP', 
                 'TA', 'TKEY', 'TLSA', 'TSIG', 'TXT', 'URI']


def end(msg):
    print(msg)
    sys.exit(1)

def create_dns_rec(domain, type):
    try:
        answ = dns_resolve.query(domain, type)
        # print(type, ' :', list(map(lambda a: a.address if type in ['A', 'AAAA'] else \
        #         a, answ)))
        return list(map(lambda a: a.address if type in ['A', 'AAAA'] else \
                a, answ))

    except dns.resolver.NXDOMAIN:
        end(f': {domain}')
        
    except Exception as e:
        # if isinstance(e, dns.resolver.NoAnswer) \
        #    or isinstance(e, dns.resolver.NoNameservers):
        #     print(f'check {type}: -')
        # elif isinstance(e, dns.rdatatype.UnknownRdatatype):
        #     print(f'check {type}: - (unknown)')
        # elif isinstance(e, dns.resolver.NoMetaqueries):
        #     print(f'check {type}: - (not allowed)')
        # else:
        #     raise e

        return None

def dump_dns(domain):
    
    # for domain in domains:
    # print('domain: ', domain)

    dns_answers = {}
    answer_list = []
    for type in dns_rec_types:
        answers = create_dns_rec(domain, type)
        if answers is not None:
            dns_answers[type] = answers
    answer_list.append(dns_answers)

    subdomains = list()
    for i, dns_answers in enumerate(answer_list):
        # print(f'\nDNS Records found for {domain}:')
        found_types = list(dns_answers.keys())
        # found_types.sort()
        for type in found_types:
            # print(' ', type)
            for rdata in dns_answers[type]:
                # print('. ', rdata)
                rdata = str(rdata).split(' ')
                for i in rdata:
                    if domain in i:
                        subdomains.append(i)
    return subdomains



    