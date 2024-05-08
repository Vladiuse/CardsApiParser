import requests as req
from requests.exceptions import RequestException, ProxyError
from print_color import print as cprint
from funcs import sleep


def check_network():
    """Проверить наличие интернет соединения"""
    try:
        req.get('https://google.com/')
    except RequestException:
        raise ConnectionError('Интернет не работает')


PROXY_CKECK_TRY_COUNT = 3


def check_proxy(proxy):
    """Проверить работает ли прокси"""
    get_ip_url = 'https://api.ipify.org?format=json'
    proxies = {
        'https': proxy.url
    }
    sleep_time = 5
    for try_num in range(PROXY_CKECK_TRY_COUNT):
        try_num += 1
        try:
            res = req.get(get_ip_url, proxies=proxies)
            if res.status_code != 200:
                print(f'Не удалось получить айпи (status code {res.status_code}) ({try_num}/{PROXY_CKECK_TRY_COUNT})')
                sleep(sleep_time)
                sleep_time += 5
            else:
                ip = res.json()['ip']
                text = f'Proxy IP: {ip}'
                cprint(text, color='blue')
                return
        except RequestException:
            print(f'RequestException, не получилось подключитсья к прокси ({try_num}/{PROXY_CKECK_TRY_COUNT})')
            sleep(sleep_time)
            sleep_time += 5
    else:
        raise ConnectionError('Прокси не работает')


if __name__ == '__main__':
    url = 'http://CazGYr:naaRax3YR6ez@pproxy.space:17022/'

    check_proxy(url)
