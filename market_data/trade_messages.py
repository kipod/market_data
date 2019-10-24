from .common import DATA_SIZE
from .trade import Trade


class TradeMessages(object):
    def __init__(self, trade_file):
        self.trade_file = trade_file
        self.__curr_message = None
        Trade._manager = self

    def get_next_message(self):
        with open(self.trade_file, 'br') as f:
            byte_data = f.read(DATA_SIZE)
            while byte_data:
                self.__curr_message = Trade.parse(byte_data)
                assert self.__curr_message, 'ERROR: Wrong trade file "{}" ???'.format(self.trade_file)
                yield self.__curr_message
                byte_data = f.read(DATA_SIZE)

    def __repr__(self):
        return "file: {}".format(self.trade_file)
