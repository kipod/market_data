from .common import str_time_from_timestamp

TP_TRADE_FULL = 0x0004
TP_TRADE_LONG = 0x0005
TP_CONDITIONALTRADE_FULL = 0x000C
TP_CONDITIONALTRADE_LONG = 0x000D
TP_TRADE_CANCEL = 0x0006
TP_TRADE_CORRECTION = 0x0007

LEGAL_TYPES = (
    TP_TRADE_FULL,
    TP_TRADE_LONG,
    TP_CONDITIONALTRADE_FULL,
    TP_CONDITIONALTRADE_LONG,
    TP_TRADE_CANCEL,
    TP_TRADE_CORRECTION
)


class Trade(object):
    _manager = None

    def __init__(self, protocol_type, message_type, symbol_id, t2, size, price, side):
        self.protocol_type = protocol_type
        self.message_type = message_type
        self.symbol_id = symbol_id
        self.t2 = t2
        self.size = size
        self.price = price
        self.side = side

    @staticmethod
    def is_support(protocol_type, message_type):
        return protocol_type == 2 and message_type in LEGAL_TYPES

    @staticmethod
    def parse(data: bytes) -> object:
        protocol_type = int.from_bytes(data[0:2], byteorder='little', signed=False)
        message_type = int.from_bytes(data[2:4], byteorder='little', signed=False)
        if not Trade.is_support(protocol_type, message_type):
            return None
        symbol_id = int.from_bytes(data[4:8], byteorder='little', signed=False)
        t2 = int.from_bytes(data[12:20], byteorder='little', signed=False)
        trade_size = int.from_bytes(data[20:24], byteorder='little', signed=False)
        trade_price = int.from_bytes(data[24:28], byteorder='little', signed=False)
        trade_side = data[28:29].decode('utf-8')
        return Trade(protocol_type, message_type, symbol_id, t2, trade_size, trade_price, trade_side)

    def __eq__(self, order):
        if order.is_execute:
            return self.price == order.price and self.size == order.size
        return False
        # return self.bid_volume == other.bid_volume and self.bid_price == other.bid_price and \
        #        self.ask_price == other.ask_price and self.ask_volume == other.ask_volume

    def __repr__(self):
        res = 'TRADE '
        res += 'size: {} '.format(self.size)
        res += 'price: {} '.format(self.price)
        res += 'T={}'.format(str_time_from_timestamp(self.t2, True))
        return res
