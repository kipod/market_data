# new
TP_ADD_ORDER_BUY_LONG = 0x0001
TP_ADD_ORDER_SELL_LONG = 0x0002
# delete
TP_CANCEL_ORDER_LONG = 0x0004
TP_CANCEL_ORDER_FULL = 0x0005
TP_DELETE_ORDER = 0x0006
# modify
TP_MODIFY_ORDER_LONG = 0x0007
TP_MODIFY_ORDER_FULL = 0x0008
TP_REPLACE_ORDER_LONG = 0x000D
TP_REPLACE_ORDER_FULL = 0x000E
TP_ADD_ORDER_ATTR_BUY_LONG = 0x0010
TP_ADD_ORDER_ATTR_SELL_LONG = 0x0011
TP_ADD_ORDER_ATTR_FULL = 0x0012
# execute
TP_EXEC_ORDER_NP_FV = 0x0009
TP_EXEC_ORDER_NP_LV = 0x000A
TP_EXEC_ORDER_LP_LV = 0x000B
TP_EXEC_ORDER_FP_FV = 0x000C
TP_EXEC_ORDER_WREMAINING_LONG = 0x0013
TP_EXEC_ORDER_WREMAINING_FULL = 0x0014

LEGAL_TYPES = (
    TP_ADD_ORDER_BUY_LONG,
    TP_ADD_ORDER_SELL_LONG,
    TP_CANCEL_ORDER_LONG,
    TP_CANCEL_ORDER_FULL,
    TP_DELETE_ORDER,
    TP_MODIFY_ORDER_LONG,
    TP_MODIFY_ORDER_FULL,
    TP_REPLACE_ORDER_LONG,
    TP_REPLACE_ORDER_FULL,
    TP_ADD_ORDER_ATTR_BUY_LONG,
    TP_ADD_ORDER_ATTR_SELL_LONG,
    TP_ADD_ORDER_ATTR_FULL,
    TP_EXEC_ORDER_NP_FV,
    TP_EXEC_ORDER_NP_LV,
    TP_EXEC_ORDER_LP_LV,
    TP_EXEC_ORDER_FP_FV,
    TP_EXEC_ORDER_WREMAINING_LONG,
    TP_EXEC_ORDER_WREMAINING_FULL
)

NEW_ORDER_TYPES = (
    TP_ADD_ORDER_BUY_LONG,
    TP_ADD_ORDER_SELL_LONG
)

DELETE_ORDER_TYPES = (
    TP_CANCEL_ORDER_LONG,
    TP_CANCEL_ORDER_FULL,
    TP_DELETE_ORDER,
    TP_EXEC_ORDER_NP_FV,
    TP_EXEC_ORDER_NP_LV,
    TP_EXEC_ORDER_LP_LV,
    TP_EXEC_ORDER_FP_FV
)

MODIFY_ORDER_TYPE = (
    TP_MODIFY_ORDER_LONG,
    TP_MODIFY_ORDER_FULL,
    TP_REPLACE_ORDER_LONG,
    TP_REPLACE_ORDER_FULL,
    TP_EXEC_ORDER_WREMAINING_LONG,
    TP_EXEC_ORDER_WREMAINING_FULL
)


class Order(object):
    _manager = None

    def __init__(self, protocol_type, message_type, symbol_id, t2, order_id, size, price, side):
        self.protocol_type = protocol_type
        self.message_type = message_type
        self.symbol_id = symbol_id
        self.t2 = t2
        self.order_id = order_id
        self.size = size
        self.price = price
        self.side = side
        self.update_book()

    @staticmethod
    def is_support(protocol_type, message_type):
        return protocol_type == 1 and message_type in (
            TP_ADD_ORDER_BUY_LONG,
            TP_ADD_ORDER_SELL_LONG,
            TP_CANCEL_ORDER_LONG,
            TP_CANCEL_ORDER_FULL,
            TP_DELETE_ORDER,
        )

    @staticmethod
    def parse(data: bytes) -> object:
        protocol_type = int.from_bytes(data[0:2], byteorder='little', signed=False)
        message_type = int.from_bytes(data[2:4], byteorder='little', signed=False)
        if not Order.is_support(protocol_type, message_type):
            return None
        symbol_id = int.from_bytes(data[4:8], byteorder='little', signed=False)
        t2 = int.from_bytes(data[12:20], byteorder='little', signed=False)
        order_id = int.from_bytes(data[20:28], byteorder='little', signed=False)
        if message_type in NEW_ORDER_TYPES:
            order_size = int.from_bytes(data[28:32], byteorder='little', signed=False)
            order_price = int.from_bytes(data[32:36], byteorder='little', signed=False)
            side = 'B' if message_type == TP_ADD_ORDER_BUY_LONG else 'S'
        elif message_type in DELETE_ORDER_TYPES:
            orig_order = Order._manager.order_by_id(order_id)
            order_size = orig_order.size if orig_order is not None else None
            order_price = orig_order.price if orig_order is not None else None
            side = orig_order.side if orig_order is not None else None
        else:
            orig_order = Order._manager.order_by_id(order_id)
            side = orig_order.side if orig_order is not None else None
            order_size = int.from_bytes(data[28:32], byteorder='little', signed=False)
            order_price = int.from_bytes(data[32:36], byteorder='little', signed=False)
            if not order_size:
                order_size = orig_order.size if orig_order is not None else None
            if not order_price:
                order_price = orig_order.price if orig_order is not None else None
        return Order(protocol_type, message_type, symbol_id, t2, order_id, order_size, order_price, side)

    def update_book(self):
        if self.message_type in NEW_ORDER_TYPES:
            self._manager.add_order(self)
        elif self.message_type in DELETE_ORDER_TYPES:
            self._manager.del_order(self.order_id)
        elif self.message_type in MODIFY_ORDER_TYPE:
            order = self._manager.order_by_id(self.order_id)
            if self.size:
                order.size = self.size
            if self.price:
                order.price = self.price
        else:
            assert False, 'Unknown message type'
        pass

    def __repr__(self):
        action = '???'
        if self.message_type in NEW_ORDER_TYPES:
            action = 'NEW'
        elif self.message_type in DELETE_ORDER_TYPES:
            action = 'DEL'
        elif self.message_type in MODIFY_ORDER_TYPE:
            action = 'EDIT'
        return "{} side: {} size:{} price:{}".format(action, self.side, self.size, self.price)
