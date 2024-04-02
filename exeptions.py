from print_color import print as cprint
from pprint import pprint
class ToManyReqErrors(Exception):
    """Превышен лимит ошибок запросов в сеть подряд"""

    def __init__(self, errors_count: int):
        self.errors_count = errors_count

    def __str__(self):
        text = self.__doc__ + f' ({self.errors_count}шт.)'
        cprint(text, tag=self.__class__.__name__, color='white', tag_color='red')
        return ''


class EmptyAdsLibResponse(Exception):

    def __init__(self, data=None):
        self.data = data

    def __str__(self):
        for key in ('errorSummary', 'errorDescription'):
            try:
                text = self.data[key]
                cprint(text, tag=key, color='white', tag_color='red')
            except KeyError:
                pass
        text = 'Empty payload'
        cprint(text, tag=self.__class__.__name__, color='white', tag_color='red')
        return ''

class LibEnds(Exception):

    def __str__(self):
        text = 'Библиотека закончилась (пустой forwardCursor)'
        cprint(text, tag=self.__class__.__name__, color='white', tag_color='red')
        return ''

if __name__ == '__main__':
    raise LibEnds
