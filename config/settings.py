import os
from .config import config

PC_NAME = config.get('Pc', 'name')
LOG_FILE_DIR_PATH = config.get('Loger', 'log_dir_path')
LOG_FILE_NAME = f'{PC_NAME}_links.txt'
LOG_FILE_PATH = os.path.join(LOG_FILE_DIR_PATH, LOG_FILE_NAME)
DB_PATH = config.get('DB', 'db_file_path')

REQ_ERRORS_ROW_COUNT = int(config.get('AdsLibParser', 'req_errors_row_count'))
REQ_TIMEOUT = int(config.get('AdsLibParser', 'req_timeout'))
SLEEP_BETWEEN_REQS = int(config.get('AdsLibParser', 'sleep_between_reqs'))

PLAY_SOUND = True if config.get('Pc', 'play_sound')  == 'true' else False


KEY_WORDS_TYPES = ('vocabulary', 'chars')

KEYWORD_TYPE = config.get('KeyWords', 'keys_type')
if KEYWORD_TYPE not in KEY_WORDS_TYPES:
    raise ValueError(f'Incorrect keys type "{KEYWORD_TYPE}", must be {KEY_WORDS_TYPES}')



