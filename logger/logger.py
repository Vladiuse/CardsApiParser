from print_color import print as cprint
from funcs import Timer
from config.settings import LOG_FILE_PATH

timer = Timer()


def log_links(card_res):
    with open(LOG_FILE_PATH, 'a', encoding='utf-8') as log_file:
        log_file.write(timer.time_string + '\n')
        for card in card_res:
            log_file.write(f'{card.fb_group_url}\n')
            # log_file.write(f'{card.ad_archive_id} {card.page_name} {card.fb_group_url}\n')
        log_file.write('************\n')
    if len(card_res) > 25:
        color = 'green'
    elif len(card_res) >= 10:
        color = 'yellow'
    else:
        color = 'red'
    print(timer.time_string)
    cprint(f'Log {len(card_res)} links ' + '#' * len(card_res), color=color)
