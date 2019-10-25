from .common import str_time_from_timestamp

TP_TOP_OF_BOOK_NWBBO = 0x001B
TP_TOP_OF_BOOK_NWBBO_FULL = 0x001A
TP_TOP_OF_BOOK_BBO_WV = 0x0018
TP_TOP_OF_BOOK_BBO_FULL_WV = 0x0019

LEGAL_TYPES = (
    TP_TOP_OF_BOOK_NWBBO,
    TP_TOP_OF_BOOK_NWBBO_FULL,
    TP_TOP_OF_BOOK_BBO_WV,
    TP_TOP_OF_BOOK_BBO_FULL_WV,
)


class BBO(object):
    _manager = None

    def __init__(self, protocol_type, message_type, symbol_id, t2, bid_volume, bid_price, ask_price, ask_volume):
        self.protocol_type = protocol_type
        self.message_type = message_type
        self.symbol_id = symbol_id
        self.t2 = t2
        self.bid_volume = bid_volume
        self.bid_price = bid_price
        self.ask_price = ask_price
        self.ask_volume = ask_volume

    @staticmethod
    def is_support(protocol_type, message_type):
        return protocol_type == 4 and message_type in LEGAL_TYPES

    @staticmethod
    def parse(data: bytes) -> object:
        protocol_type = int.from_bytes(data[0:2], byteorder='little', signed=False)
        message_type = int.from_bytes(data[2:4], byteorder='little', signed=False)
        if not BBO.is_support(protocol_type, message_type):
            return None
        symbol_id = int.from_bytes(data[4:8], byteorder='little', signed=False)
        t2 = int.from_bytes(data[12:20], byteorder='little', signed=False)
        bid_volume = int.from_bytes(data[20:24], byteorder='little', signed=False)
        bid_price = int.from_bytes(data[24:28], byteorder='little', signed=False)
        ask_price = int.from_bytes(data[28:32], byteorder='little', signed=False)
        ask_volume = int.from_bytes(data[32:36], byteorder='little', signed=False)
        return BBO(protocol_type, message_type, symbol_id, t2, bid_volume, bid_price, ask_price, ask_volume)

    # @property
    # def delta(self):
    #     return self._manager.get_delta_message()

    def __eq__(self, other):
        return self.bid_volume == other.bid_volume and self.bid_price == other.bid_price and \
               self.ask_price == other.ask_price and self.ask_volume == other.ask_volume

    def __repr__(self):
        res = ""
        res += 'bid: {} '.format(self.bid_price)
        res += 'ask: {} '.format(self.ask_price)
        res += 'bid_vol: {} '.format(self.bid_volume)
        res += 'ask_vol: {} '.format(self.ask_volume)
        res += 'T={}'.format(str_time_from_timestamp(self.t2, True))
        return res
