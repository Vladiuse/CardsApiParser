from datetime import datetime
from datetime import timedelta
from countries import countries
from keywords import get_random_keyword
import random as r


class FbAdsLibUrl:
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

    def __init__(self, country, q, start_date=None, media_type=None, active_status=None):
        self._country = country
        self.q = q
        self.start_date = start_date if start_date else str(datetime.now().date() - timedelta(days=1))
        self.media_type = media_type if media_type else 'all'
        self.active_status = active_status if active_status else 'all'

    def __str__(self):
        params =  f'active_status={self.active_status}&ad_type=all&country={self._country.iso}&q={self.q}&publisher_platforms[0]=facebook&sort_data[direction]=desc&sort_data[mode]=relevancy_monthly_grouped&start_date[min]={self.start_date}&start_date[max]=&search_type=keyword_unordered&media_type={self.media_type}'
        return FbAdsLibUrl.URL + '?'+ params

    def __repr__(self):
        print('FbLibUrl Params')
        print(f'Q:{self.q}')
        print(f'Country: {self._country}')
        print(f'StartDate: {self.start_date}')
        print(f'MediaType: {self.media_type}')
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
        if self.media_type not in FbAdsLibUrl.MEDIA_TYPES:
            raise ValueError('Incorrect mediaType param')

    def _check_active_status(self):
        if self.active_status not in FbAdsLibUrl.ACTIVE_STATUS_TYPES:
            raise ValueError('Incorrect active status')

def get_random_url():
    c = countries.get_random()
    q = get_random_keyword()
    active_status = r.choice(['active', 'inactive'])
    media_type = r.choice(['video', 'image'])
    return FbAdsLibUrl(
        country=c,
        q=q,
        media_type=media_type,
        start_date='2024-01-01',
        active_status=active_status,
    )

if __name__ == '__main__':
    url = get_random_url()
    print(repr(url))
    print(url)
