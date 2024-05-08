from config.config import config


proxies_data = config.items('Proxy')
for proxy_id, proxy in proxies_data:
    print(proxy_id, proxy)