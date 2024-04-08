import requests as req
from requests.exceptions import RequestException, ProxyError
from print_color import print as cprint

def check_network():
    try:
        req.get('https://google.com/')
    except RequestException:
        raise ConnectionError('Интернет не работает')

def check_proxy(proxy):
    get_ip_url = 'https://api.ipify.org?format=json'
    proxies = {
        'https': proxy.url
    }
    try:
        res = req.get(get_ip_url, proxies=proxies)
        if res.status_code != 200:
            print(f'Не удалось получить айпи (status code {res.status_code})')
        else:
            ip = res.json()['ip']
            text = f'Proxy IP: {ip}'
            cprint(text, color='blue')
    except RequestException:
        raise ConnectionError('Прокси не работает')


if __name__ == '__main__':
    url= 'http://CazGYr:naaRax3YR6ez@pproxy.space:17022/'

    check_proxy(url)
