from copy import copy
from collections import deque
from .common import DATA_SIZE, MAX_LATENCY_TIME
from .order import Order


class MarketMessages(object):
    def __init__(self, file_market):
        self.__messages = deque()
        self.file_market = file_market
        self.__last_t2_in_buffer = 0
        self.__last_matched_message_t2 = 0
        self.orders = {}  # by order id
        self.gen_bbo = None
        self.prev_gen_bbo = None
        Order._manager = self
        self.next_message_from_file = self.___next_message_from_file()

    def is_match(self, order, bbo) -> bool:
        assert self and order and bbo
        self.update_gen_bbo(order)
        return self.gen_bbo == bbo

    def find_match_message(self, bbo):
        if self.gen_bbo is None:
            self.gen_bbo = bbo
            return None
        else:
            self.prev_gen_bbo = copy(self.gen_bbo)

        # remove old messages from queue
        while self.__messages:
            t2 = self.__messages[0].t2
            if t2 <= self.__last_matched_message_t2 or abs(t2 - bbo.t2) > MAX_LATENCY_TIME:
                self.__messages.popleft()
            else:
                break

        # bbo_delta = bbo_message.delta
        # if bbo_delta is None:
        #     return None

        # search in queue
        for order in self.__messages:
            if self.is_match(order, bbo):
                self.__last_matched_message_t2 = order.t2
                self.gen_bbo = bbo
                return order

        for order in self.next_message_from_file:
            if order.t2 > bbo.t2:
                break
            if self.is_match(order, bbo):
                self.__last_matched_message_t2 = order.t2
                self.gen_bbo = bbo
                return order

        # self.gen_bbo = self.prev_gen_bbo
        self.gen_bbo = bbo
        return None

    def ___next_message_from_file(self):
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

    def update_gen_bbo(self, message):
        ask_price, ask_volume, bid_price, bid_volume = \
            message.get_update_bbo(self.gen_bbo)
        if self.gen_bbo.ask_price > ask_price:
            self.gen_bbo.ask_price = ask_price
            if ask_price <= self.gen_bbo.bid_price and \
                    not [o for o in self.orders.values() if o.side == 'B' and o.symbol_id == message.symbol_id]:
                self.gen_bbo.bid_price = ask_price - 100
            else:
                self.gen_bbo.bid_price = bid_price
            self.gen_bbo.ask_volume = ask_volume
            self.gen_bbo.bid_volume = bid_volume
        elif self.gen_bbo.bid_price < bid_price:
            self.gen_bbo.bid_price = bid_price
            if bid_price >= self.gen_bbo.ask_price and \
                    not [o for o in self.orders.values() if o.side == 'S' and o.symbol_id == message.symbol_id]:
                self.gen_bbo.ask_price = bid_price + 100
            else:
                self.gen_bbo.ask_price = ask_price
            self.gen_bbo.ask_volume = ask_volume
            self.gen_bbo.bid_volume = bid_volume
        else:
            self.gen_bbo.ask_price = ask_price
            self.gen_bbo.ask_volume = ask_volume
            self.gen_bbo.bid_price = bid_price
            self.gen_bbo.bid_volume = bid_volume

    def __repr__(self):
        return "file: {}".format(self.file_market)
