from exeptions import parser_dead

COMMANDS = [
    {
        'name': 'parse.py {-proxy=proxy_num}',
        'description': 'Парсить либу'
    },
    {
        'name': 'show_countries.py',
        'description': 'Список стран'
    },
    {
        'name': 'show_proxies.py',
        'description': 'Список прокси'
    },
]
for command in COMMANDS:
    print(command['name'])
    print('-', command['description'], end='\n\n')

