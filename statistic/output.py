from market_data.common import str_time_from_timestamp, time_from_timestamp, time_in_seconds
from .interval import Interval
from datetime import time

INTERVAL_SECONDS = 30


class Output(object):
    def __init__(self, file_name: str = 'out.csv'):
        self.file_name = file_name
        self.__file = open(file_name, 'wt')
        self.__interval = None

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
        # self.__file.write('{},{}\n'.format(str_time_from_timestamp(quote_time), delta))

    def get_interval(self, dt):
        t = dt.time()

        need_new_interval = self.__interval is None
        if not need_new_interval:
            if time_in_seconds(t) - time_in_seconds(self.__interval.start_time) > INTERVAL_SECONDS:
                self.__interval.write_to_file(self.__file)
                need_new_interval = True

        if need_new_interval:
            self.__interval = Interval(time(t.hour, t.minute, INTERVAL_SECONDS if t.second > INTERVAL_SECONDS else 0))
        
        return self.__interval






