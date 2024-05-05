import whois

list_field = {"domain_name": "domain_name", "registrar": "registrar", "updated_date": "updated_date",
                  "creation_date": "creation_date", "expiration_date": "expiration_date",
                  "name_servers": "name_servers", "dnssec": "dnssec", "name": "name", "org": "org",
                  "address": "address", "city": "city", "state": "state", "zipcode": "zipcode", "country": "country"}

def get_whois_inf(domain):
    whois_dict = dict()
    try:
        wh = whois.whois(domain, flags=0)
        # print(wh)
        for field in list_field:
            date = []
            if wh.get(field) is not None:
                try:
                    if field == 'updated_date':
                        for dat in wh.get(field):
                            date.append(dat)
                            if str(wh[field]) not in whois_dict:
                                whois_dict[list_field[field]] = date

                    elif field == 'creation_date':
                        for dat in wh.get(field):
                            date.append(dat)
                            if str(wh[field]) not in whois_dict:
                                whois_dict[list_field[field]] = date

                    elif field == 'expiration_date':
                        for dat in wh.get(field):
                            date.append(dat)
                            if str(wh[field]) not in whois_dict:
                                whois_dict[list_field[field]] = date

                    else:
                        if str(wh[field]) not in whois_dict:
                            whois_dict[list_field[field]] = wh[field]

                except TypeError:
                    if str(wh[field]) not in whois_dict:
                        whois_dict[list_field[field]] = str(wh[field])

    except whois.parser.PywhoisError:
        return whois_dict

    return whois_dict
