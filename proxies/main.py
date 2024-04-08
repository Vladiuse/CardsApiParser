import requests as req
from requests.exceptions import RequestException

class Proxy:

    def __init__(self, id, url, change_ip_url):
        self.id = id
        self.url = url
        self.change_ip_url = change_ip_url

    def __repr__(self):
        return f'Proxy {self.id}\n{self.url}'

    def change_ip(self):
        print('Change proxy ip')
        for _ in range(2):
            try:
                res = req.get(self.change_ip_url, timeout=30)
                if res.status_code == 200:
                    print(res.text)
                    break
                else:
                    print('Change ip res not 200!', res.status_code)
            except RequestException as error:
                print('Change Ip error', error)
