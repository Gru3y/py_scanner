import argparse

parser = argparse.ArgumentParser(description="Simple TCP/UDP Scanner")
parser.add_argument('adres', type=str, help='IP address')
parser.add_argument('-sT', action='store_true', help='TCP Scan')
parser.add_argument('-sU', action='store_true', help='UDP Scan')

args = parser.parse_args()