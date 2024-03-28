from datetime import datetime
from datetime import timedelta
from countries import countries

class FbAdsLibUrl:
    URL = 'https://www.facebook.com/ads/library/'
    MEDIA_TYPES = {
        'all',
        'image',
        'video',
    }

    def __init__(self, country, q, start_date=None, media_type=None):
        self.country = country
        self.q = q
        self.start_date = start_date if start_date else str(datetime.now().date() - timedelta(days=1))
        self.media_type = media_type if media_type else 'all'

    def __str__(self):
        params =  f'active_status=all&ad_type=all&country={self.country.iso}&q={self.q}&sort_data[direction]=desc&sort_data[mode]=relevancy_monthly_grouped&start_date[min]={self.start_date}&start_date[max]=&search_type=keyword_unordered&media_type={self.media_type}'
        return FbAdsLibUrl.URL + '?'+ params

    def __repr__(self):
        print('FbLibUrl Params')
        print(f'Q:{self.q}')
        print(f'Country: {self.country}')
        print(f'StartDate: {self.start_date}')
        print(f'MediaType: {self.media_type}')
        return '\n'
    def _check_params(self):
        self._check_media_type_param()

    def _check_media_type_param(self):
        if self.media_type not in FbAdsLibUrl.MEDIA_TYPES:
            raise ValueError('Incorrect mediaType param')



if __name__ == '__main__':
    print(countries)
    c = countries['US']
    q = '123'
    url = FbAdsLibUrl(c,q=q, start_date='2024-03-27', media_type='video')
    print(repr(url))

