import nmap
import sys


def nmap_A_scan(network_prefix):
    nm = nmap.PortScanner()
    # Настроить параметры сканирования nmap
    scan_raw_result = nm.scan(hosts=network_prefix, arguments='-v -n -A')
    # Анализировать результаты сканирования
    for host, result in scan_raw_result['scan'].items():
        if result['status']['state'] == 'up':
            print('#' * 17 + 'Host:' + host + '#' * 17)
            print('-' * 20 + "Предположение операционной системы" + '-' * 20)
            
            # Проверка наличия ключа 'osmatch'
            if 'osmatch' in result:
                for os in result['osmatch']:
                    print("Операционная система:" + os['name'] + ' ' * 3 + "Точность:" + os['accuracy'])
            else:
                print("Операционная система не была определена.")
            idno = 1
            try:
                for port in result['tcp']:
                    try:
                        print('-' * 17 + "Детали TCP-сервера" + '[' + str(idno) + ']' + '-' * 17)
                        idno += 1
                        print('Номер порта TCP:' + str(port))
                        try:
                            print('положение дел:' + result['tcp'][port]['state'])
                        except:
                            pass
                        try:
                            print('причина:' + result['tcp'][port]['reason'])
                        except:
                            pass
                        try:
                            print('Дополнительная информация:' + result['tcp'][port]['extrainfo'])
                        except:
                            pass
                        try:
                            print('Имя:' + result['tcp'][port]['name'])
                        except:
                            pass
                        try:
                            print('версия:' + result['tcp'][port]['version'])
                        except:
                            pass
                        try:
                            print('товар:' + result['tcp'][port]['product'])
                        except:
                            pass
                        try:
                            print('CPE：' + result['tcp'][port]['cpe'])
                        except:
                            pass
                        try:
                            print("Сценарий:" + result['tcp'][port]['script'])
                        except:
                            pass
                    except:
                        pass
            except:
                pass

            idno = 1
            try:
                for port in result['udp']:
                    try:
                        print('-' * 17 + "Детали сервера UDP" + '[' + str(idno) + ']' + '-' * 17)
                        idno += 1
                        print('Номер порта UDP:' + str(port))
                        try:
                            print('положение дел:' + result['udp'][port]['state'])
                        except:
                            pass
                        try:
                            print('причина:' + result['udp'][port]['reason'])
                        except:
                            pass
                        try:
                            print('Дополнительная информация:' + result['udp'][port]['extrainfo'])
                        except:
                            pass
                        try:
                            print('Имя:' + result['udp'][port]['name'])
                        except:
                            pass
                        try:
                            print('версия:' + result['udp'][port]['version'])
                        except:
                            pass
                        try:
                            print('товар:' + result['udp'][port]['product'])
                        except:
                            pass
                        try:
                            print('CPE：' + result['udp'][port]['cpe'])
                        except:
                            pass
                        try:
                            print("Сценарий:" + result['udp'][port]['script'])
                        except:
                            pass
                    except:
                        pass
            except:
                print("skip")
                pass


if __name__ == '__main__':
    nmap_A_scan('aid.mirea.ru')