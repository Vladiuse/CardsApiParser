import os
from .config import config, ConfigError
from datetime import datetime, timedelta
import random as r

PC_NAME = config.get('Pc', 'name')
LOG_FILE_DIR_PATH = config.get('Loger', 'log_dir_path')
LOG_FILE_NAME = f'{PC_NAME}_links.txt'
LOG_FILE_PATH = os.path.join(LOG_FILE_DIR_PATH, LOG_FILE_NAME)
DB_PATH = config.get('DB', 'db_file_path')

REQ_ERRORS_ROW_COUNT = int(config.get('AdsLibParser', 'req_errors_row_count'))
REQ_TIMEOUT = int(config.get('AdsLibParser', 'req_timeout'))
SLEEP_BETWEEN_REQS = int(config.get('AdsLibParser', 'sleep_between_reqs'))

PLAY_SOUND = True if config.get('Pc', 'play_sound') == 'true' else False

KEY_WORDS_TYPES = ('vocabulary', 'chars')

KEYWORD_TYPE = config.get('KeyWords', 'keys_type')
if KEYWORD_TYPE not in KEY_WORDS_TYPES:
    raise ValueError(f'Incorrect keys type "{KEYWORD_TYPE}", must be {KEY_WORDS_TYPES}')


class AdsLib:
    _START_DATE = config.get('AdsLib', 'start_date')
    _END_DATE = config.get('AdsLib', 'end_date')
    _FLOATING_END_DATE = config.get('AdsLib', 'floating_end_date')

    TODAY = datetime.today().date()
    FLOATING_DATA_VALUES = ('true', 'false')

    @classmethod
    def START_DATE(cls):
        return str(cls._to_date(cls._START_DATE))

    @classmethod
    def END_DATE(cls):
        if not cls.FLOATING_END_DATE():
            return str(cls._to_date(cls._END_DATE))
        else:
            return cls._get_float_end_date()

    @staticmethod
    def _to_date(date: str, date_name=None):
        if date == 'today':
            return AdsLib.TODAY
        else:
            try:
                return datetime.strptime(date, '%Y-%m-%d').date()
            except ValueError:
                raise ConfigError(f'Incorrect {date_name}')

    @classmethod
    def FLOATING_END_DATE(cls):
        if cls._FLOATING_END_DATE == 'true':
            return True
        if cls._FLOATING_END_DATE == 'false':
            return False

    @classmethod
    def validate(cls):
        cls._check_start_date()
        cls._check_end_date()
        cls._check_floating_data()

    @staticmethod
    def _check_start_date():
        if AdsLib._START_DATE == 'today':
            return
        start_date = AdsLib._to_date(AdsLib._START_DATE, 'start_date')
        if start_date > AdsLib.TODAY:
            raise ConfigError('start_date cant be more than today date')

    @staticmethod
    def _check_end_date():
        end_date = AdsLib._to_date(AdsLib._END_DATE, 'end_date')
        if end_date > AdsLib.TODAY:
            raise ConfigError('end_date cant be more than today date')
        start_date = AdsLib._to_date(AdsLib._START_DATE, 'start_date')
        if end_date < start_date:
            raise ConfigError('end_date cant be more than start_date')

    @staticmethod
    def _check_floating_data():
        if AdsLib._FLOATING_END_DATE not in AdsLib.FLOATING_DATA_VALUES:
            raise ConfigError(f'Incorrect floating_end_date, must be in {AdsLib.FLOATING_DATA_VALUES}')

    @classmethod
    def dates(cls) -> tuple:
        if not cls.FLOATING_END_DATE():
            return (cls.START_DATE(), cls.END_DATE())
        else:
            return (cls.START_DATE(), cls._get_float_end_date())

    @classmethod
    def _get_float_end_date(csl):
        if not csl.FLOATING_END_DATE():
            raise AttributeError('Floating slag must be True')
        start_date = AdsLib._to_date(AdsLib._START_DATE, 'start_date')
        end_date = AdsLib._to_date(AdsLib._END_DATE, 'end_date')
        diff = end_date - start_date
        new_days_delta = r.randint(0, diff.days)
        # return new_days_delta
        return str(start_date + timedelta(days=new_days_delta))

AdsLib.validate()