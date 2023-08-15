import argparse
import socket

parser = argparse.ArgumentParser(description="Simple TCP/UDP Scanner")
parser.add_argument('address', type=str, help='IP address')
parser.add_argument('-sT', action='store_true', help='TCP Scan')
parser.add_argument('-sU', action='store_true', help='UDP Scan')
parser.add_argument('-p', type=int, help='Port to scan')

args = parser.parse_args()


'''def main():
    pass'''


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
    pass

tcp_scan()

'''if __name__ == '__main__':
    main()'''


'''
if args.sT:
    
    
elif args.sU:
    print('UDP Scan')
'''