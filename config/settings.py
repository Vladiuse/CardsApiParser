import os
from .config import config

PC_NAME = config.get('Pc', 'name')
LOG_FILE_DIR_PATH = config.get('Loger', 'log_dir_path')
LOG_FILE_NAME = f'{PC_NAME}_links.txt'
LOG_FILE_PATH = os.path.join(LOG_FILE_DIR_PATH, LOG_FILE_NAME)

REQ_ERRORS_ROW_COUNT = int(config.get('AdsLibParser', 'req_errors_row_count'))
REQ_TIMEOUT = int(config.get('AdsLibParser', 'req_timeout'))

