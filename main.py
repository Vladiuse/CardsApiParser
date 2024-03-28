from time import sleep
import requests as req
from requests.exceptions import RequestException
from urllib.parse import urlparse, parse_qs
import urllib.parse
from pprint import pprint
import json
from logger import log_links, log_tokens, get_old_tokens
from cards_resp import FbCardsRes, fb_responce_to_dict

proxies = {
    'https': 'http://CazGYr:naaRax3YR6ez@pproxy.space:17022/' # 1
}
REQ_TIMEOUT = 30
USE_PROXY = False
USE_OLD_TOKENS = False

if USE_PROXY:
    REQ_KWARGS = {
        'proxies': proxies
    }
else:
    REQ_KWARGS = {}
basic_cookies = {
    'wd': '1920x325',
}
headers = {
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
    print(result)
    return result

GEO = input('Enter Geo: ')
if len(GEO) != 2:
    raise ValueError('Incorrect geo len!')
Q = urllib.parse.quote('coll some today')
url = f'https://www.facebook.com/ads/library/?active_status=all&ad_type=all&country={GEO}&q=*&sort_data[direction]=desc&sort_data[mode]=relevancy_monthly_grouped&start_date[min]=2024-02-29&start_date[max]=&search_type=keyword_unordered&media_type=all'
param_string = url.split('?')[-1]
param_string = param_string.replace('country', 'countries[0]')
print(param_string)

res = req.get(url, headers=headers,cookies=basic_cookies,timeout=REQ_TIMEOUT,**REQ_KWARGS)
if res.status_code != 200:
    print('Not 200 status code')
    raise ConnectionError

html = res.text
with open('x.html', 'w') as file:
    file.write(html)

basic_params = get_basic_params(html)
basic_cookies.update({
    'datr': basic_params['datr']
})
headers.update(
    {
        'origin': 'https://www.facebook.com',
        'referer': url,
        'content-type': 'application/x-www-form-urlencoded'
    })

data = {
    '__aaid': '0',
    '__user': '0',
    '__a': '1',
    '__req': '2',
    '__hs': basic_params['hs'],
    'dpr': '2',
    '__ccg': 'EXCELLENT',
    '__rev': basic_params['rev'],
    '__hsi': basic_params['hsi'],
    'lsd': basic_params['lsd'],
    '__spin_r': basic_params['spin_r'],
    '__spin_b': basic_params['spin_b'],
    '__spin_t': basic_params['spin_t'],
}


forward_cursor = None
collation_token = None


SLEEP_TIME = 1
REQUEST_COUNT = 0
while True:
    sleep(SLEEP_TIME)
    if not forward_cursor:
        print('First req without tokens')
        cards_url = f'https://www.facebook.com/ads/library/async/search_ads/?session_id={basic_params["session_id"]}&count=30&' + param_string
    else:
        cards_url = f'https://www.facebook.com/ads/library/async/search_ads/?forward_cursor={forward_cursor}&backward_cursor=&session_id={basic_params["session_id"]}&collation_token={collation_token}&count=30&{param_string}'
    for _ in range(5):
        try:
            res = req.post(
                cards_url,
                headers=headers,
                data=data,
                cookies=basic_cookies,
                timeout=REQ_TIMEOUT,
                **REQ_KWARGS,
            )
            res_text = res.text
            if not res.status_code == 200:
                with open('error_not_200.json', 'w') as file:
                    file.write(res_text)
                print('Responce not 200!')
                sleep(5)
                continue
            else:
                break
        except RequestException as error:
            print(error)
            print('Continue')
    else:
        print('5 error requests')
        print(("*"*30 + "\n") * 5)
        print(GEO)
        raise RequestException
    #######
    with open('x.json', 'w') as file:
        file.write(res_text)
    REQUEST_COUNT += 1
    print('REQUEST_COUNT',REQUEST_COUNT)
    cards_data = fb_responce_to_dict(res_text)
    cards_res = FbCardsRes(cards_data)
    log_links(cards_res)
    # [print(card) for card in cards_res]
    cards_res.show_tokens()
    print('*********************')
    if REQUEST_COUNT == 1 and USE_OLD_TOKENS:
        print('Use old tokens')
        forward_cursor, collation_token = get_old_tokens()
        print( forward_cursor, collation_token, sep='\n')
    else:
        forward_cursor = cards_res.forward_cursor
        collation_token = cards_res.collation_token
        log_tokens(forward_cursor, collation_token)


