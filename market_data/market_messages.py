from collections import deque
from .const import DATA_SIZE, MAX_LATENCY_TIME
from .order import Order


class MarketMessages(object):
    def __init__(self, file_market):
        self.__messages = deque()
        self.file_market = file_market
        self.__last_t2_in_buffer = 0
        self.__last_matched_message_t2 = 0
        self.orders = {}  # by order id
        Order._manager = self

    def is_match(self, order, bbo_delta) -> bool:
        assert self and order and bbo_delta
        if bbo_delta is None:
            return False

        # TODO
        return False

    def find_match_message(self, bbo_message):
        # remove old messages from queue
        while self.__messages:
            t2 = self.__messages[0].t2
            if t2 < self.__last_matched_message_t2 or (t2 - bbo_message.t2) > MAX_LATENCY_TIME:
                self.__messages.popleft()
            else:
                break

        bbo_delta = bbo_message.delta
        if bbo_delta is None:
            return None

        # search in queue
        for message in self.__messages:
            if self.is_match(message, bbo_delta):
                self.__last_matched_message_t2 = message.t2
                return message

        for message in self.next_message_from_file():
            if message.t2 > bbo_message.t2:
                return None
            if self.is_match(message, bbo_delta):
                self.__last_matched_message_t2 = message.t2
                return message

        return None

    def next_message_from_file(self):
        with open(self.file_market, 'br') as f:
            byte_data = f.read(DATA_SIZE)
            while byte_data:
                msg = Order.parse(byte_data)
                assert msg, 'ERROR: Wrong file "{}" ???'.format(self.file_market)
                self.__last_t2_in_buffer = msg.t2
                self.__messages.append(msg)
                yield msg
                byte_data = f.read(DATA_SIZE)

    def add_order(self, order):
        """ new order """
        self.orders[order.order_id] = order

    def del_order(self, order_id: int):
        """remove order from book"""
        del self.orders[order_id]

    def order_by_id(self, order_id):
        return self.orders[order_id] if order_id in self.orders else None
