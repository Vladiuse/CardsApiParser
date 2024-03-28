class ToManyReqErrors(Exception):
    """Превышен лимит ошибок запросов в сеть подряд"""

    def __init__(self, errors_count: int):
        self.errors_count = errors_count

    def __str__(self):
        return self.__doc__ + f' {self.errors_count}шт'


class EmptyAdsLibResponse(Exception):

    def __str__(self):
        return 'Empty payload'


class LibEnds(Exception):

    def __str__(self):
        return 'Библиотека закончилась (пустой forwardCursor)'


raise EmptyAdsLibResponse
