from fbadslib.fbadslib_url import get_random_url
from fbadslib.fbadslib_page import FbAdsLibPage
from logger.logger import log_links, log_tokens, get_old_tokens
from exeptions import *


class FbAdsLibParser:

    def __init__(self):
        self.parsed_pages_count = 0

    def _parse_lib_page(self):
        url = get_random_url()
        fbadslib_page = FbAdsLibPage(url)
        fbadslib_page.open()
        for cards in fbadslib_page.parse_cards():
            log_links(cards)
            print('*********************\n')

    def parse_lib(self):
        while True:
            try:
                self.parsed_pages_count += 1
                self._parse_lib_page()
            except (LibEnds, ToManyReqErrors) as error:
                print(error)


if __name__ == '__main__':
    parser = FbAdsLibParser()
    parser.parse_lib()
