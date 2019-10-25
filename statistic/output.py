from datetime import time

from market_data.common import time_from_timestamp, time_in_seconds
from .interval import Interval

DEFAULT_INTERVAL_SECONDS = 30


class Output(object):
    def __init__(self, file_name: str = 'out.csv', interval_seconds=DEFAULT_INTERVAL_SECONDS):
        self.file_name = file_name
        self.__file = open(file_name, 'wt')
        self.__interval = None
        self.interval_seconds = interval_seconds

    def __enter__(self):
        Interval.print_title(self.__file)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        self.__file.close()

    def __del__(self):
        self.close()

    def __repr__(self):
        return "file: {}".format(self.file_name)

    def add_stats(self, market_time, quote_time):
        dt = time_from_timestamp(quote_time)
        
        # assert quote_time > market_time
        delta = quote_time - market_time
        self.get_interval(dt).add_point(delta)

    def get_interval(self, dt):
        t = dt.time()

        need_new_interval = self.__interval is None
        if not need_new_interval:
            if time_in_seconds(t) - time_in_seconds(self.__interval.start_time) > self.interval_seconds:
                self.__interval.write_to_file(self.__file)
                need_new_interval = True

        if need_new_interval:
            self.__interval = Interval(
                time(t.hour, t.minute, self.interval_seconds if t.second > self.interval_seconds else 0)
            )
        
        return self.__interval
