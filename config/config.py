import os
from configparser import ConfigParser, NoOptionError
from proxies import Proxy
from print_color import print as cprint

conf_file_path = './conf.ini'
config = ConfigParser()
config.read(conf_file_path, encoding='utf-8')

class ConfigError(Exception):
    pass
def get_proxy_from_conf(proxy_id):
    try:
        proxy_url = config.get('Proxy', proxy_id)
        proxy_change_ip_url = config.get('ProxyChangeIpUrl', proxy_id)
        proxy = Proxy(proxy_id, proxy_url, proxy_change_ip_url)
        return proxy
    except NoOptionError as error:
        cprint('Incorrect proxy id', color='white', tag='ProxyNotExist', tag_color='red')
        exit()
