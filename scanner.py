import argparse
import socket
import pyfiglet
from ping3 import ping

def parse_port_range(port_range):
    print(port_range)
    start, end = map(int, port_range.split('-'))
    if 1 <= start <= 65535 and 1 < end <= 65535 and start < end:
        port_range_list = list(range(start, end + 1))
    return port_range_list

def perform_ping(ip_addr):
    reply = ping(ip_addr)
    if reply is not None:
        return f"{ip_addr} is reachable."
    else:
        return f"{ip_addr} is not reachable."



def tcp_scan(args):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_scan_result = False
    try:
        r = sock.connect_ex((args.address, args.p))
        if r == 0:
            sock.close()
            print(f"Port TCP {args.p} is open.")
            tcp_scan_result = True
            return tcp_scan_result
        else:
            print(f"Port TCP {args.p} is closed.")
            return tcp_scan_result
    except OverflowError:
        print('Port must be 0-65535')
    except socket.gaierror:
        print('Invalid hostname or IPv4 address.')
    

def udp_scan(args):
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

def tcp_top_ports_scan(args):
    top_ports = [21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 443, 445, 993, 995, 1433, 1723, 3306, 3389, 5432, 5900, 8080]
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

def scan_port_range(args):
    open_ports = []
    for port in args.range:
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

def banner_grabber(args):
        tcp_scan_result = tcp_scan(args)
        if tcp_scan_result:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect_ex((args.address, args.p))
            try:
                if args.p == 80:
                    sock.sendto(b'GET / HTTP/1.1\r\n\r\n', (args.address, args.p))
                    header = sock.recv(1024)
                    lines = header.split(b'\r\n')
                    for line in lines:
                        if line.startswith(b"Server:"):
                            print(line.decode('utf-8'))
                else:
                    data = sock.recv(1024)
                    print(data.strip().decode('utf-8'))
            except Exception as e:
                print(f'Something went wrong. {e}')
        else:
            print('Port TCP is closed, so i dont grab the banner.')
        #print(data.decode('utf-8'))

def main():
    header = pyfiglet.figlet_format('PyScanner')
    print(header)

    parser = argparse.ArgumentParser(description="Simple TCP/UDP Port Scanner")

    parser.add_argument('address', type=str, help='IP address') 
    parser.add_argument('-sT', action='store_true', help='TCP Scan') 
    parser.add_argument('-sU', action='store_true', help='UDP Scan') 
    parser.add_argument('-tp', action='store_true', help='Top ports scan')
    parser.add_argument('-b', action='store_true', help='Banner grabbing')
    parser.add_argument('-p', type=int, help='Port to scan') 
    parser.add_argument('-r', type=parse_port_range, help='Range of ports to scan (e.g. 20-100)')

    args, unknown_args = parser.parse_known_args()
    print(args)

    try:
        if unknown_args:
            print(f"Unrecognized parameters: {unknown_args}")
        elif args.sT and args.r:
            scan_port_range(args)
        #elif args.sT:
            #tcp_scan(args)
        elif args.sT and args.b:
            banner_grabber(args)
        elif args.top_ports:
            tcp_top_ports_scan(args)
        elif args.sU:
            udp_scan(args)
    except argparse.ArgumentError:
        print('Fatal Parse Error')


if __name__ == '__main__':
    main()