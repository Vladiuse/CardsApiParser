from time import sleep as _sleep

def sleep(time:int, show=True):
    if show:
        print(f'Sleep {time}...')
    _sleep(time)
