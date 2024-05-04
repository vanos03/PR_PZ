import psycopg2
from gevent import exceptions
from ping3 import ping

def get_subdomains_in_cert(domain):
    sub_dom = set()

    try:
        conn = psycopg2.connect(host="crt.sh", database="certwatch", user="guest", port="5432")
    except psycopg2.OperationalError as e:
        print(f"Failed get subdomains: {e}")
        return None
    conn.autocommit = True
    cur = conn.cursor()
    query = f"SELECT ci.NAME_VALUE NAME_VALUE FROM certificate_identity ci WHERE ci.NAME_TYPE = 'dNSName' AND " \
            f"reverse(lower(ci.NAME_VALUE)) LIKE reverse(lower('%.{domain}')) "
    cur.execute(query)
    result = cur.fetchall()
    cur.close()
    conn.close()

    if len(result) > 0:
        for item in result:
            print(item)
            if "*" not in item[0]:
                try:
                    p = ping(item[0])
                    if p != False:
                        sub_dom.add(item[0])
                        print("[+]", item[0])
                    else:
                        print("[-]", item[0])
                except exceptions.LoopExit:
                    return None

    return sub_dom
