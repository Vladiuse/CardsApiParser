from print_color import print as cprint
from funcs import Timer
from config.settings import LOG_FILE_PATH, PC_NAME, LOG_FILE_DIR_PATH
import os
timer = Timer()


def log_links(card_res, country_code=None):
    if country_code:
        file_name = f'{PC_NAME}_{country_code.upper()}_links.txt'
    else:
        file_name = f'{PC_NAME}_links.txt'
    file_save_path = os.path.join(LOG_FILE_DIR_PATH, file_name)
    with open(file_save_path, 'a', encoding='utf-8') as log_file:
        # log_file.write(timer.time_string + '\n')
        for card in card_res:
            log_file.write(f'{card.fb_group_url}\n')
            # log_file.write(f'{card.group_id}\t{card.ad_archive_id}\t{card.fb_group_url}\n')
        # log_file.write('************\n')
    if len(card_res) > 25:
        color = 'green'
    elif len(card_res) >= 10:
        color = 'yellow'
    else:
        color = 'red'
    print(timer.time_string)
    cprint(f'Log {len(card_res)} links ' + '#' * len(card_res), color=color)
