from fbadslib_url import get_random_url
from fbadslib_page import FbAdsLibPage
from logger.logger import log_links, log_tokens, get_old_tokens
from exeptions import *
from funcs import Timer, check_network

check_network()
timer = Timer()
def parse_lib_page():
    url = get_random_url()
    fbadslib_page = FbAdsLibPage(url)
    fbadslib_page.open()
    for cards in fbadslib_page.parse_cards():
        log_links(cards)
        print('*********************\n')



def infy_parse():
    while True:
        try:
            parse_lib_page()
        except (LibEnds,ToManyReqErrors) as error:
            print(error)

infy_parse()