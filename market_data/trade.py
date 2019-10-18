class Trade(object):
    def __init__(self, protocol_type, message_type, symbol_id, t2, size, price):
        self.protocol_type = protocol_type
        self.message_type = message_type
        self.symbol_id = symbol_id
        self.t2 = t2
        self.size = size
        self.price = price

    @staticmethod
    def is_support(protocol_type, message_type):
        return protocol_type == 2 and message_type in (4, 5, 0xC, 0xD, 6, 7)

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
        return Trade(protocol_type, message_type, symbol_id, t2, trade_size, trade_price)
