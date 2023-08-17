import argparse
import socket
import pyfiglet
from ping3 import ping

parser = argparse.ArgumentParser(description="Simple TCP/UDP Port Scanner")
parser.add_argument('address', type=str, help='IP address')
parser.add_argument('-sT', action='store_true', help='TCP Scan')
parser.add_argument('-sU', action='store_true', help='UDP Scan')
#parser.add_argument('-p-', '--top-ports' action='store_true', help='Top ports scan')
parser.add_argument('-p', type=int, help='Port to scan')

args = parser.parse_args()

def main():
    header = pyfiglet.figlet_format('PyScanner')
    print(header)
    '''if args.sT:
        tcp_scan()
    
    elif args.sU:
        udp_scan()'''

def tcp_scan():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        r = sock.connect_ex((args.address, args.p))
        if r == 0:
            sock.close()
            print(f"Port TCP {args.p} is open.")
        else:
            print(f"Port TCP {args.p} is closed.")
    except OverflowError:
        print('Port must be 0-65535')
    except socket.gaierror:
        print('Invalid hostname or IPv4 address.')

def udp_scan():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(1)
    try:
        reach_addr = perform_ping(args.address)
        sock.sendto(b'Payload', (args.address, args.p))
        sock.recvfrom(1024)
        print('Port is open.')
    except TimeoutError or ConnectionResetError:
        print(f"The server didn't respond but the scanned port may be open. {reach_addr}")
    except OverflowError:
        print('Port must be 0-65535')
    except socket.gaierror:
        print('Invalid hostname or IPv4 address.')
    finally:
        sock.close()

def tcp_top_ports():
    top_ports = [21, 22, 23, 25, 53, 80, 110, 111, 139, 143, 443, 445, 993, 995, 1433, 1723, 3306, 3389, 5432, 5900, 8080]
    open_ports = []
    
    for port in top_ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            r = sock.connect_ex((args.address, port))
            if r == 0:
                open_ports.append(port)
            sock.close()
        except:
            pass

    print(open_ports)
            
def perform_ping(ip_addr):
    reply = ping(ip_addr)
    if reply is not None:
        return f"{ip_addr} is reachable."
    else:
        return f"{ip_addr} is not reachable."


'''if __name__ == '__main__':
    main()'''