import nmap
import sys


def nmap_A_scan(network_prefix):
    nm = nmap.PortScanner()
    scan_raw_result = nm.scan(hosts=network_prefix, arguments='-v -n -A')

    for host, result in scan_raw_result['scan'].items():
        if result['status']['state'] == 'up':
            print('\n\nHost: ' + host )
            print("The assumption of the OC")
            
            if 'osmatch' in result:
                for os in result['osmatch']:
                    print("OC:" + os['name'])
            else:
                print("OC has not been identified")

            try:
                print( "\n\n*TCP scan details:")
                for port in result['tcp']:
                    try:
                        print('\n. TCP port:' + str(port))
                        try:
                            print('.. state:' + result['tcp'][port]['state'])
                        except:
                            pass
                        try:
                            print('.. reason:' + result['tcp'][port]['reason'])
                        except:
                            pass
                        try:
                            print('.. extrainfo:' + result['tcp'][port]['extrainfo'])
                        except:
                            pass
                        try:
                            print('.. name:' + result['tcp'][port]['name'])
                        except:
                            pass
                        try:
                            print('.. version:' + result['tcp'][port]['version'])
                        except:
                            pass
                        try:
                            print('.. product:' + result['tcp'][port]['product'])
                        except:
                            pass
                        try:
                            print('.. CPE：' + result['tcp'][port]['cpe'])
                        except:
                            print('.. CPE：' '-')
                            pass
                        try:
                            print(".. script:" + result['tcp'][port]['script'])
                        except:
                            pass
                    except:
                        pass
            except:
                pass

            try:
                print( "\n\n*UDP scan details:" )
                for port in result['udp']:
                    try:
                        print('\n. UDP port:' + str(port))
                        try:
                            print('.. state:' + result['udp'][port]['state'])
                        except:
                            pass
                        try:
                            print('.. reason:' + result['udp'][port]['reason'])
                        except:
                            pass
                        try:
                            print('.. extrainfo:' + result['udp'][port]['extrainfo'])
                        except:
                            pass
                        try:
                            print('.. name:' + result['udp'][port]['name'])
                        except:
                            pass
                        try:
                            print('.. version:' + result['udp'][port]['version'])
                        except:
                            pass
                        try:
                            print('.. product:' + result['udp'][port]['product'])
                        except:
                            pass
                        try:
                            print('.. CPE：' + result['udp'][port]['cpe'])
                        except:
                            print('.. CPE：' '-')
                            pass
                        try:
                            print(".. script:" + result['udp'][port]['script'])
                        except:
                            pass
                    except:
                        pass
            except:
                pass
