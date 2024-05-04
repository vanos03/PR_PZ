import socket
import requests

def get_web_servers(domain):
    try:
        ip_addresses = socket.gethostbyname_ex(domain)
        return ip_addresses[2]
    except socket.gaierror:
        return "Не удалось разрешить имя хоста"

    

