import argparse
from fbadslib.fbadslib_parser import FbAdsLibParser
from funcs import Timer, check_network, check_proxy
from config.config import get_proxy_from_conf
from exeptions import parser_dead


parser = argparse.ArgumentParser(description='xxxx')
parser.add_argument('-proxy', type=str, default=None, help='Proxy id')
timer = Timer()
try:
    check_network()
except ConnectionError as error:
    print(error)
    parser_dead()


args = parser.parse_args()
proxy = None
if args.proxy:
    proxy = get_proxy_from_conf(args.proxy)
    print(repr(proxy))
    try:
        check_proxy(proxy)
    except ConnectionError as error:
        print(error)
        parser_dead()

parser = FbAdsLibParser(proxy)
parser.parse_lib()
