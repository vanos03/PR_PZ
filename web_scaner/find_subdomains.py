import sublist3r

def find_subdomains(domain):

    subdomains = sublist3r.main(domain, 128, None, ports=None, 
                                silent=True, verbose=True, 
                                enable_bruteforce=False, engines=None)

    # print(subdomains)
    return subdomains

