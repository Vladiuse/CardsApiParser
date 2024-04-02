from fbadslib.fbadslib_parser import FbAdsLibParser
from funcs import Timer, check_network


check_network()
timer = Timer()

parser = FbAdsLibParser()
parser.parse_lib()