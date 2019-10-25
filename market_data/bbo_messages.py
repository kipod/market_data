from .common import DATA_SIZE
from .bbo import BBO


class BboMessages(object):
    def __init__(self, bbo_file):
        self.bbo_file = bbo_file
        self.__curr_message = None
        BBO._manager = self

    def get_next_message(self):
        with open(self.bbo_file, 'br') as f:
            byte_data = f.read(DATA_SIZE)
            while byte_data:
                self.__curr_message = BBO.parse(byte_data)
                assert self.__curr_message, 'ERROR: Wrong BBO file "{}" ???'.format(self.bbo_file)
                yield self.__curr_message
                byte_data = f.read(DATA_SIZE)

    def __repr__(self):
        return "file: {}".format(self.bbo_file)
