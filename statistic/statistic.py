from market_data.common import str_time_from_timestamp

class Statistic(object):
    def __init__(self, file_name: str = 'out.csv'):
        self.file_name = file_name
        self.__file = open(file_name, 'wt')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        self.__file.close()

    def __del__(self):
        self.close()

    def __repr__(self):
        return "file: {}".format(self.file_name)
