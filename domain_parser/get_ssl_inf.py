import socket
from datetime import datetime

import OpenSSL
from OpenSSL.SSL import Connection, Context, SSLv3_METHOD, TLSv1_2_METHOD


def get_ssl_inf(domain):
    cert_info = {}

    try:
        try:
            ssl_connection_setting = Context(SSLv3_METHOD)
        except ValueError:
            ssl_connection_setting = Context(TLSv1_2_METHOD)
        ssl_connection_setting.set_timeout(5)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((domain, 443))
            c = Connection(ssl_connection_setting, s)
            c.set_tlsext_host_name(str.encode(domain))
            c.set_connect_state()
            c.do_handshake()

            cert = c.get_peer_certificate()
            cert_info.update({'Алгоритм шифрования': cert.get_signature_algorithm().decode('utf-8')})
            cert_info.update({'Серийный номер': cert.get_serial_number()})
            cert_info.update({'Хэш имени субъекта': cert.subject_name_hash()})

            sub_list = cert.get_subject().get_components()
            issuer = cert.get_issuer().get_components()

            for item in sub_list:
                if item[0].decode('utf-8') == 'CN':
                    cert_info.update({'Кому выдан': item[1].decode('utf-8')})

            for item in issuer:
                if item[0].decode('utf-8') == 'CN':
                    cert_info.update({'Кем выдан': item[1].decode('utf-8')})
                if item[0].decode('utf-8') == 'C':
                    cert_info.update({'Страна': item[1].decode('utf-8')})
                if item[0].decode('utf-8') == 'ST':
                    cert_info.update({'Штат/Область': item[1].decode('utf-8')})
                if item[0].decode('utf-8') == 'L':
                    cert_info.update({'Город': item[1].decode('utf-8')})
                if item[0].decode('utf-8') == 'O':
                    cert_info.update({'Организация': item[1].decode('utf-8')})

            if not cert.has_expired():
                cert_info.update({'Действует до': str(datetime.strptime(str(cert.get_notAfter().decode('utf-8')),
                                                                          "%Y%m%d%H%M%SZ"))})
            else:
                cert_info.update({'Истек срок действия': str(datetime.strptime(str(cert.get_notAfter().decode('utf-8')),
                                                                 "%Y%m%d%H%M%SZ"))})
            c.shutdown()
            s.close()
            return cert_info
    except (TypeError, ConnectionRefusedError, socket.gaierror, OSError, OpenSSL.SSL.Error):
        print(f"Соединение с {domain} не удалось")
        return cert_info