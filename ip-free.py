import ipaddress
import subprocess
import sys
import time

def ping_ip(ip):
    try:
        start = time.time()
        ping = subprocess.run(
            ["ping", "-c", "1", "-W", "1", str(ip)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE
        )
        end = time.time()

        if ping.returncode == 0:
            ms = int((end - start) * 1000)
            return "UP", f"{ms}ms"
        else:
            return "DOWN", "No response"

    except Exception as e:
        return "ERROR", str(e)

def main():
    if len(sys.argv) != 2:
        print("Usage: python ip_freely.py <CIDR>")
        print("Example: python ip_freely.py 192.168.1.0/24")
        return

    cidr = sys.argv[1]

    try:
        network = ipaddress.ip_network(cidr, strict=False)
    except:
        print("Oops... that CIDR is not valid.")
        return

    print(f"Scanning network {cidr}...\n")

    up_count = 0
    down_count = 0
    err_count = 0

    for host in network.hosts():
        status, info = ping_ip(host)
        print(f"{host}  - {status} ({info})")

        if status == "UP":
            up_count += 1
        elif status == "DOWN":
            down_count += 1
        else:
            err_count += 1

    print("\nScan complete.")
    print(f"Found {up_count} active hosts, {down_count} down, {err_count} errors")

if __name__ == "__main__":
    main()
