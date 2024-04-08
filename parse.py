import argparse
from fbadslib.fbadslib_parser import FbAdsLibParser
from funcs import Timer, check_network, check_proxy
from config.config import get_proxy_from_conf


parser = argparse.ArgumentParser(description='xxxx')
parser.add_argument('-proxy', type=str, default=None, help='Proxy id')


check_network()
timer = Timer()

args = parser.parse_args()
proxy = None
if args.proxy:
    proxy = get_proxy_from_conf(args.proxy)
    check_proxy(proxy)

parser = FbAdsLibParser(proxy)
parser.parse_lib()
