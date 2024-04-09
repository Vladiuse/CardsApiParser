from time import sleep as _sleep

def sleep(time:int, show=True):
    if not isinstance(time, int):
        raise TypeError('Incorect sleep time type (must be int)')
    if show:
        print(f'Sleep {time}...')
    _sleep(time)
