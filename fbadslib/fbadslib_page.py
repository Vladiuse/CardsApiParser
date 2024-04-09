import os

from funcs import sleep
import requests as req
from requests.exceptions import RequestException
from fbadslib.cards_resp import FbCardsRes, fb_responce_to_dict
from fbadslib.fbadslib_url import  FbAdsLibUrl
from exeptions import ToManyReqErrors
from funcs import Timer, check_proxy
from config.settings import REQ_ERRORS_ROW_COUNT, REQ_TIMEOUT, SLEEP_BETWEEN_REQS



timer = Timer()

class FbAdsLibPage:
    basic_cookies = {
        'wd': '1920x325',
    }
    basic_headers = {
        'authority': 'www.facebook.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'uk-UA,uk;q=0.9,en-US;q=0.8,en;q=0.7',
        # 'cache-control': 'max-age=0',
        # 'cookie': 'datr=3yDfZY0Rti8G0kS_lPtOnutL; ps_l=0; ps_n=0; dpr=2; fr=0IwSIMg0dKkvPlr0l..Bl3y21..AAA.0.0.Bl3y3Z.AWWwVg491ek; usida=eyJ2ZXIiOjEsImlkIjoiQXM5dTQ0NWs3eXJmZSIsInRpbWUiOjE3MDk1NzQ0ODV9; wd=1920x567',
        'dpr': '2',
        'sec-ch-prefers-color-scheme': 'dark',
        'sec-ch-ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
        'sec-ch-ua-full-version-list': '"Not A(Brand";v="99.0.0.0", "Google Chrome";v="121.0.6167.75", "Chromium";v="121.0.6167.75"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-model': '""',
        'sec-ch-ua-platform': '"macOS"',
        'sec-ch-ua-platform-version': '"13.3.0"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'viewport-width': '1920',
    }

    def __init__(self, url:FbAdsLibUrl, proxy=None):
        self.url = url
        self.proxy = proxy
        self.headers = FbAdsLibPage.basic_headers.copy()
        self.cookies = FbAdsLibPage.basic_cookies.copy()
        self.basic_params  = None
        self.data = None
        self.forward_cursor = None
        self.collation_token = None
        self.REQUEST_COUNT = 0

        self.REQ_KWARGS = {
            'proxies': { 'https': self.proxy.url}
        } if self.proxy else {}

    @staticmethod
    def get_basic_params(html):
        result = dict()
        params_from_search = {
            'datr': ['"_js_datr","', '"'],
            'session_id': ['session_id":"', '"'],
            'lsd': ['"LSD",[],{"token":"', '"'],
            'hs': ['"haste_session":"', '"'],
            'rev': ['"client_revision":', ','],
            'hsi': ['"hsi":"', '"'],
            'spin_r': ['"__spin_r":', ','],
            'spin_b': ['"__spin_b":"', '"'],
            'spin_t': ['"__spin_t":', ','],
            # 'xxx': ['xxxx', 'xxxxxx'],
        }
        for param_key, search in params_from_search.items():
            try:
                start = html.index(search[0]) + len(search[0])
                end = html.index(search[1], start)
                param_value = html[start: end]
                result.update({
                    param_key: param_value
                })
            except ValueError as error:
                raise ValueError(param_key, 'параметр не найден')
        return result

    def open(self):
        print(repr(self.url))
        url_string = str(self.url)
        print(url_string)
        res = req.get(url_string,
                      headers=self.headers,
                      cookies=self.basic_cookies,
                      timeout=REQ_TIMEOUT,
                      **self.REQ_KWARGS,
                      )
        if res.status_code != 200:
            print('Not 200 status code')
            raise ConnectionError

        html = res.text
        with open('./z_work/x.html', 'w', encoding='utf-8') as file:
            file.write(html)
        self.basic_params = self.get_basic_params(html)
        self.cookies.update({
            'datr': self.basic_params['datr']
        })
        self.headers.update(
            {
                'origin': 'https://www.facebook.com',
                'referer': url_string,
                'content-type': 'application/x-www-form-urlencoded'
            })

        self.data = {
            '__aaid': '0',
            '__user': '0',
            '__a': '1',
            '__req': '2',
            '__hs': self.basic_params['hs'],
            'dpr': '2',
            '__ccg': 'EXCELLENT',
            '__rev': self.basic_params['rev'],
            '__hsi': self.basic_params['hsi'],
            'lsd': self.basic_params['lsd'],
            '__spin_r': self.basic_params['spin_r'],
            '__spin_b': self.basic_params['spin_b'],
            '__spin_t': self.basic_params['spin_t'],
        }

    def parse_cards(self):
        self.REQUEST_COUNT = 0
        while True:
            sleep(SLEEP_BETWEEN_REQS, show=False)
            if not self.forward_cursor:
                print('First req without tokens')
                cards_url = f'https://www.facebook.com/ads/library/async/search_ads/?session_id={self.basic_params["session_id"]}&count=30&' + self.url.param_string
            else:
                cards_url = f'https://www.facebook.com/ads/library/async/search_ads/?forward_cursor={self.forward_cursor}&backward_cursor=&session_id={self.basic_params["session_id"]}&collation_token={self.collation_token}&count=30&{self.url.param_string}'
            sleep_time = 5
            for _ in range(REQ_ERRORS_ROW_COUNT):
                try:
                    res = req.post(
                        cards_url,
                        headers=self.headers,
                        data=self.data,
                        cookies=self.cookies,
                        timeout=REQ_TIMEOUT,
                        **self.REQ_KWARGS,
                    )
                    res_text = res.text
                    res.raise_for_status()
                    sleep_time = 5
                    sleep(SLEEP_BETWEEN_REQS, show=False)
                    break
                except req.exceptions.HTTPError as error:
                    with open('./logs/error_not_200.json', 'w', encoding='utf-8') as file:
                        file.write(res_text)
                    print(f'Responce not 200! ({res.status_code})')
                    sleep(sleep_time)
                    sleep_time += 5
                except RequestException as error:
                    print(error)
                    print('Continue')
                    sleep(sleep_time)
                    sleep_time += 5
            else:
                print('\n' * 9)
                print(self.url.country)
                print('REQUEST_COUNT:',self.REQUEST_COUNT)
                print(timer.time_string)
                raise ToManyReqErrors
            #######
            with open('./z_work/x.json', 'w') as file:
                file.write(res_text)
            self.REQUEST_COUNT += 1
            print('REQUEST_COUNT:', self.REQUEST_COUNT)
            print(repr(self.url.country))
            cards_data = fb_responce_to_dict(res_text)
            cards_res = FbCardsRes(cards_data)
            yield cards_res








