from datetime import datetime

class Timer:
    def __init__(self):
        pass

    @property
    def time_string(self):
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        time_string = f'Time: {dt_string}'
        return time_string