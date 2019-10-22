from .const import DATA_SIZE
from .bbo import BBO


class BboMessages(object):
    def __init__(self, bbo_file):
        self.bbo_file = bbo_file
        self.__curr_message = None
        self.__prev_message = {}  # symbol_id
        BBO._manager = self

    def get_next_message(self):
        with open(self.bbo_file, 'br') as f:
            byte_data = f.read(DATA_SIZE)
            while byte_data:
                if self.__curr_message:
                    self.__prev_message[self.__curr_message.symbol_id] = self.__curr_message
                self.__curr_message = BBO.parse(byte_data)
                assert self.__curr_message, 'ERROR: Wrong BBO file "{}" ???'.format(self.bbo_file)
                yield self.__curr_message
                byte_data = f.read(DATA_SIZE)

    # def get_delta_message(self):
    #     symbol_id = self.__curr_message.symbol_id
    #     prev_bbo = self.__prev_message[symbol_id] if symbol_id in self.__prev_message else None
    #     if prev_bbo is None:
    #         return None
    #     return BBODelta(0, 0, symbol_id,
    #                     self.__curr_message.t2 - prev_bbo.t2,
    #                     self.__curr_message.bid_volume - prev_bbo.bid_volume,
    #                     self.__curr_message.bid_price - prev_bbo.bid_price,
    #                     self.__curr_message.ask_price - prev_bbo.ask_price,
    #                     self.__curr_message.ask_volume - prev_bbo.ask_volume
    #                     )

    def __repr__(self):
        return "file: {}".format(self.bbo_file)


# class BBODelta(BBO):
#     def __init__(self, protocol_type, message_type, symbol_id, t2, bid_volume, bid_price, ask_price, ask_volume):
#         super().__init__(protocol_type, message_type, symbol_id, t2, bid_volume, bid_price, ask_price, ask_volume)
#
#     def __repr__(self):
#         res = ""
#         if self.bid_price:
#             res += 'bid: {}'.format(self.bid_price)
#         if self.ask_price:
#             res += 'ask: {}'.format(self.ask_price)
#         if self.ask_volume:
#             res += 'ask_vol: {}'.format(self.ask_volume)
#         if self.bid_volume:
#             res += 'ask_vol: {}'.format(self.bid_volume)
#         return res
