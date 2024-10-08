import re
from datetime import datetime
from datetime import timedelta
from countries import countries
from keywords import get_random_char_keyword, keyword_db,  get_random_word_from_file
import random as r
from config.settings import KEYWORD_TYPE, AdsLib
from urllib.parse import quote
from countries import countries


class FbAdsLibUrl:

    @property
    def param_string(self):
        raise NotImplemented

    @property
    def country(self):
        raise NotImplemented

class FbAdsLibUrlString(FbAdsLibUrl):

    def __init__(self, url):
        self.url = url
        self.q = 'Не определен'

    def __str__(self):
        return self.url

    @property
    def param_string(self):
        return self.url.split('?')[-1]

    @property
    def country(self):
        result = re.search('country=\w\w', self.url)
        if result:
            country_url_param = result[0]
            country_code = country_url_param.split('=')[-1]
            country = countries[country_code]
            return country
        else:
            raise ValueError('cant find country in url')

class FbAdsLibUrlBuilder(FbAdsLibUrl):
    URL = 'https://www.facebook.com/ads/library/'
    MEDIA_TYPES = {
        'all',
        'image',
        'video',
    }
    ACTIVE_STATUS_TYPES = {
        'all',
        'active',
        'inactive',
    }

    def __init__(self, country, q,
                 start_date=None,
                 end_date=None,
                 media_type=None,
                 active_status=None,
                 ):
        self._country = country
        self.q = q
        self.start_date = start_date if start_date else str(datetime.now().date() - timedelta(days=1))
        self.end_date = end_date if end_date else ''
        self.media_type = media_type if media_type else 'all'
        self.active_status = active_status if active_status else 'all'

    def __str__(self):
        escaped_q = quote(str(self.q), safe="")
        params = f'active_status={self.active_status}&ad_type=all&country={self._country.iso}&q={escaped_q}&publisher_platforms[0]=facebook&sort_data[direction]=desc&sort_data[mode]=relevancy_monthly_grouped&start_date[min]={self.start_date}&start_date[max]={self.end_date}&search_type=keyword_unordered&media_type={self.media_type}'
        return FbAdsLibUrlBuilder.URL + '?' + params

    def __repr__(self):
        print('FbLibUrl Params')
        print(f'Q:{repr(self.q)}')
        print(f'Country: {repr(self._country)}')
        print(f'StartDate: {self.start_date}')
        print(f'End Date: {self.end_date}')
        print(f'MediaType: {self.media_type}')
        print(f'ActiveStatus: {self.active_status}')
        return '\n'

    @property
    def param_string(self):
        params = str(self).split('?')[-1]
        params = params.replace('country', 'countries[0]')
        return params

    @property
    def country(self):
        return self._country

    def _check_params(self):
        self._check_media_type_param()

    def _check_media_type_param(self):
        if self.media_type not in FbAdsLibUrlBuilder.MEDIA_TYPES:
            raise ValueError('Incorrect mediaType param')

    def _check_active_status(self):
        if self.active_status not in FbAdsLibUrlBuilder.ACTIVE_STATUS_TYPES:
            raise ValueError('Incorrect active status')


def get_random_char_url():
    """парс на символах"""
    c = countries.get_random()
    q = get_random_char_keyword()
    media_type = r.choice(['video', 'image'])
    return FbAdsLibUrlBuilder(
        country=c,
        q=q,
        media_type=media_type,
        start_date=AdsLib.START_DATE(),
        end_date=AdsLib.END_DATE(),
        active_status=AdsLib.ADS_STATUS(),
    )

def get_random_word_url():
    """парс на символах"""
    c = countries.get_random()
    q = get_random_word_from_file()
    return FbAdsLibUrlBuilder(
        country=c,
        q=q,
        start_date=AdsLib.START_DATE(),
        end_date=AdsLib.END_DATE(),
        active_status=AdsLib.ADS_STATUS(),
    )


def get_random_keyword_url():
    """Парс по языковым ключам"""
    c = countries.get_random()
    lang = c.get_random_lang()
    q = keyword_db.get_random_key(lang.iso, (1, lang.keys_deep))
    media_type = 'all'  # r.choice(['video', 'image'])
    url = FbAdsLibUrlBuilder(
        country=c,
        q=q,
        media_type=media_type,
        start_date=AdsLib.START_DATE(),
        end_date=AdsLib.END_DATE(),
        active_status=AdsLib.ADS_STATUS(),
    )
    return url

def get_url_from_string():
    url_string = input('Enter FbLibUrl: ')
    url = FbAdsLibUrlString(url_string)
    return url



def get_url():
    """Получить ссылку на либо в зависимости от типа указаного в конциге"""
    keywords_funcs = {
        'vocabulary': get_random_keyword_url,
        'chars': get_random_char_url,
        'file_keywords': get_random_word_url,
        'input': get_url_from_string,
    }
    url_func = keywords_funcs[KEYWORD_TYPE]
    url = url_func()
    return url


if __name__ == '__main__':
    url = get_random_char_url()
    print(repr(url))
    print(url)
