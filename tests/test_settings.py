from datetime import datetime, timedelta
import unittest
from config.settings import AdsLib
from config.config import ConfigError
from unittest.mock import patch


class DateSettingsTest(unittest.TestCase):

    def test_start_date_today_text(self):
        AdsLib._START_DATE = 'today'
        AdsLib._END_DATE = '2024-01-01'
        AdsLib._FLOATING_DATE = 'false'
        try:
            AdsLib._check_start_date()
        except ConfigError:
            self.fail()

    def test_get_today_date(self):
        AdsLib._START_DATE = 'today'
        AdsLib._END_DATE = '2024-01-01'
        AdsLib._FLOATING_DATE = 'false'
        self.assertEquals(AdsLib._to_date(AdsLib._START_DATE, 'x'), AdsLib.TODAY)

    def test_start_date_incorrect_format(self):
        AdsLib._START_DATE = '1'
        AdsLib._END_DATE = '2024-01-01'
        AdsLib._FLOATING_DATE = 'false'
        with self.assertRaises(ConfigError):
            AdsLib._check_start_date()

    def test_start_date_more_today(self):
        future = datetime.today().date() + timedelta(days=1)
        AdsLib._START_DATE = str(future)
        AdsLib._END_DATE = '2024-01-01'
        AdsLib._FLOATING_DATE = 'false'
        with self.assertRaises(ConfigError):
            AdsLib._check_start_date()

    def test_end_date_incorrect_format(self):
        AdsLib._START_DATE = '2024-01-01'
        AdsLib._END_DATE = '2024-01-00'
        AdsLib._FLOATING_DATE = 'false'
        with self.assertRaises(ConfigError):
            AdsLib._check_end_date()

    def test_end_date_more_tah_today(self):
        future = datetime.today().date() + timedelta(days=1)
        AdsLib._START_DATE = '2024-01-01'
        AdsLib._END_DATE = str(future)
        AdsLib._FLOATING_DATE = 'false'
        with self.assertRaises(ConfigError):
            AdsLib._check_end_date()

    def test_end_more_than_start(self):
        AdsLib._START_DATE = '2024-01-01'
        AdsLib._END_DATE = '2023-01-01'
        AdsLib._FLOATING_DATE = 'false'
        with self.assertRaises(ConfigError):
            AdsLib._check_end_date()

    def test_incorrect_floating_flag(self):
        AdsLib._START_DATE = '2023-01-01'
        AdsLib._END_DATE = '2024-01-01'
        AdsLib._FLOATING_DATE = 'fa'
        with self.assertRaises(ConfigError):
            AdsLib._check_floating_data()

    def test_all_floating_true(self):
        AdsLib._START_DATE = '2023-01-01'
        AdsLib._END_DATE = '2024-01-01'
        AdsLib._FLOATING_DATE = 'true'
        self.assertTrue(AdsLib.FLOATING_DATE())


    def test_floating_false(self):
        AdsLib._START_DATE = '2023-01-01'
        AdsLib._END_DATE = '2024-01-01'
        AdsLib._FLOATING_DATE = 'false'
        self.assertFalse(AdsLib.FLOATING_DATE())

    def test_dates_not_floating(self):
        AdsLib._START_DATE = '2023-01-01'
        AdsLib._END_DATE = '2024-01-01'
        AdsLib._FLOATING_DATE = 'false'
        self.assertEquals(AdsLib.dates(), ('2023-01-01', '2024-01-01'))

    def test_float_end_date_not_floating(self):
        AdsLib._START_DATE = '2023-01-01'
        AdsLib._END_DATE = '2024-01-01'
        AdsLib._FLOATING_DATE = 'false'
        with self.assertRaises(AttributeError):
            AdsLib._get_float_end_date()

    def test_call_all_checkers(self):
        AdsLib._START_DATE = '2024-01-01'
        AdsLib._END_DATE = '2024-01-10'
        AdsLib._FLOATING_DATE = 'true'
        funcs = (
            '_check_start_date',
            '_check_end_date',
            '_check_floating_data',
        )
        for func in funcs:
            with patch.object(AdsLib, func) as mock:
                AdsLib.validate()
                self.assertTrue(mock.called, msg=f'Func {func} not called')