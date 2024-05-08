from print_color import print as cprint
from pprint import pprint
from config import settings
from playsound import playsound as _playsound


def playsound(*args, **kwargs):
    if settings.PLAY_SOUND:
        _playsound(*args, **kwargs)

class ToManyReqErrors(Exception):
    """Превышен лимит ошибок запросов в сеть подряд"""

    def __init__(self):
        self.errors_count = settings.REQ_ERRORS_ROW_COUNT

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
                cprint(text, tag=key, color='white', tag_color='yellow')
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

DETH_SCREEN = """
@       @  @       @ @       @ @       @  @       @ @       @ 
 @     @    @     @   @     @   @     @    @     @   @     @    
  @   @      @   @     @   @     @   @      @   @     @   @      
   @ @        @ @       @ @       @ @        @ @       @ @      
    @          @         @         @          @         @       
   @ @        @ @       @ @       @ @        @ @       @ @    
  @   @      @   @     @   @     @   @      @   @     @   @       
 @     @    @     @   @     @   @     @    @     @   @     @   
@       @  @       @ @       @ @       @  @       @ @       @ 
"""

def parser_dead():
    print(DETH_SCREEN)
    playsound('./media/parser_dead.mp3')



if __name__ == '__main__':
    raise EmptyAdsLibResponse({'errorSummary':1, 'errorDescription': 2})