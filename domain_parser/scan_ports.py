import socket

def get_service_name(port):
    try:
        service_name = socket.getservbyport(port)
        return service_name
    except OSError:
        return "Unknown"

def scan_ports(remote_host):
    open_ports = []
    try:
        for port in range(20, 443):
            print(port)
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                socket.setdefaulttimeout(1)
                result = s.connect_ex((remote_host, port))
                if result == 0:
                    service_name = get_service_name(port)
                    open_ports.append((port, service_name))
    except (socket.timeout, socket.error) as e:
        print(f"Error scanning port: {e}")
    return open_ports

remote_host = "google.com"

open_ports = scan_ports(remote_host)
if open_ports:
    print(f"Open ports on {remote_host}:")
    for port, service_name in open_ports:
        print(f"Port: {port}, Service: {service_name}")
else:
    print("No open ports found.")
