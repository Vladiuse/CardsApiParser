from datetime import datetime

LOG_FILE = 'links.txt'

def log_links(card_res):
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    time_string = f'Time: {dt_string}'
    with open(LOG_FILE, 'a') as log_file:
        log_file.write(time_string + '\n')
        # log_file.write(f'forward_cursor: {card_res.forward_cursor}\n')
        # log_file.write(f'collation_token: {card_res.collation_token}\n')
        for card in card_res:
            #log_file.write(f'{card.fb_group_url}\n')
            log_file.write(f'{card.ad_archive_id} {card.page_name} {card.fb_group_url}\n')
        log_file.write('************\n')

    print(time_string)
    print(f'Log {len(card_res)} links')

def log_tokens(a,b):
    with open('tokens.txt', 'w') as file:
        file.write(a + '\n')
        file.write(b)


def get_old_tokens():
    with open('tokens.txt') as file:
        forward_cursor, collation_token = file.read().split('\n')
        return forward_cursor, collation_token

def get_links_from_log_file():
    links_count = 0
    with open('/home/vlad/DD/links.txt', 'w') as new_file:
        with open(LOG_FILE, ) as log_file:
            for line in log_file:
                try:
                    start =  line.index('https://')
                    url = line[start:]
                    url = url.strip()
                    new_file.write(url + '\n')
                    links_count += 1
                except ValueError:
                    print(line)
    print('Links Count', links_count)


if __name__ == '__main__':
    get_links_from_log_file()
