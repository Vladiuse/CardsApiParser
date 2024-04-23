from fbadslib.fbadslib_url import get_random_url, get_random_keyword_url
from fbadslib.fbadslib_page import FbAdsLibPage
from logger.logger import log_links
from exeptions import *
from funcs import sleep


class FbAdsLibParser:

    def __init__(self, proxy=None):
        self.proxy=proxy
        self.parsed_pages_count = 0

    def _parse_lib_page(self):
        url = get_random_keyword_url()
        #url = get_random_url()
        country = url.country
        fbadslib_page = FbAdsLibPage(url, self.proxy)
        fbadslib_page.open()
        for cards in fbadslib_page.parse_cards():
            log_links(cards, country.iso)
            fbadslib_page.forward_cursor = cards.forward_cursor
            fbadslib_page.collation_token = cards.collation_token
            print('*********************\n')

    def parse_lib(self):
        while True:
            try:
                self.parsed_pages_count += 1
                self._parse_lib_page()
            except ToManyReqErrors as error:
                print(error)
            except LibEnds as error:
                print(error)
                sleep(5)
            except EmptyAdsLibResponse as error:
                if self.proxy:
                    self.proxy.change_ip()
                else:
                    raise error



if __name__ == '__main__':
    parser = FbAdsLibParser()
    parser.parse_lib()
