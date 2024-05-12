import nmap
import sys


def nmap_A_scan(network_prefix):
    nm = nmap.PortScanner()
    # Настроить параметры сканирования nmap
    scan_raw_result = nm.scan(hosts=network_prefix, arguments='-v -n -A -p 1-1024')
    cpe = list()
    for host, result in scan_raw_result['scan'].items():
        try:
            for port in result['tcp']:
                try:
                    if result['tcp'][port]['version'] != None:
                        # print('..  CPE：' + result['tcp'][port]['cpe']+ result['tcp'][port]['version'])
                        cpe.append(str(result['tcp'][port]['cpe']+ result['tcp'][port]['version']))
                except:
                    pass

                for port in result['udp']:
                    try:
                        if result['tcp'][port]['version'] != None:
                            cpe.append(str(result['udp'][port]['cpe']+ result['tcp'][port]['version']))
                            # print('..  CPE：' + result['udp'][port]['cpe']+ result['tcp'][port]['version'])
                    except:
                        pass
        except:
            pass
    return cpe


if __name__ == '__main__':
    print(nmap_A_scan('admin.digital-office.mirea.ru'))