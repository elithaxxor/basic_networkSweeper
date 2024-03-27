import os
import platform
import socket
import subprocess

# Function to get the default gateway (router IP)
def get_default_gateway():
    route_command = "ip route"  # Linux-specific command
    route_output = subprocess.check_output(route_command, shell=True).decode()
    for line in route_output.splitlines():
        if 'default' in line or '0.0.0.0' in line:
            return line.split()[2]
    return None

# Function to ping an IP address
def ping(ip):
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', param, '1', ip]
    return subprocess.call(command, stdout=subprocess.DEVNULL) == 0

# Function to get the hostname from an IP address
def get_hostname(ip):
    try:
        return socket.gethostbyaddr(ip)[0]
    except socket.herror:
        return None

# Function to ping all devices on the network and get their hostnames
def ping_all_devices(gateway):
    base_ip = '.'.join(gateway.split('.')[:-1])
    devices = {}
    for i in range(1, 255):
        ip = f"{base_ip}.{i}"
        if ping(ip):
            hostname = get_hostname(ip)
            if hostname:
                devices[ip] = hostname
            else:
                devices[ip] = 'Unknown'
    return devices

# Get the default gateway

if __name__ == '__main__':
    gateway = get_default_gateway()
    print("Gateway:", gateway)
    if gateway:
        print(f"Default Gateway (Router IP): {gateway}")
        print("Pinging all devices on the network and retrieving hostnames...")
        devices = ping_all_devices(gateway)
        print("Devices found:", devices)
        # for ip, hostname in devices.items():
        #     print(f"{hostname} - {ip}")
    else:
        print("Could not find the default gateway.")