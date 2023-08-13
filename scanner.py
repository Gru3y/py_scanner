import argparse
import socket

parser = argparse.ArgumentParser(description="Simple TCP/UDP Scanner")
parser.add_argument('address', type=str, help='IP address')
parser.add_argument('-sT', action='store_true', help='TCP Scan')
parser.add_argument('-sU', action='store_true', help='UDP Scan')
parser.add_argument('-p', type=int, help='Port to scan')

args = parser.parse_args()

if args.sT:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    r = sock.connect_ex((args.address, args.p))
    if r == 0:
        result = r
        print(f"Port TCP {args.p} is open")
        sock.close()
    else:
        print(f"Port TCP {args.p} is closed")
    
elif args.sU:
    print('UDP Scan')
