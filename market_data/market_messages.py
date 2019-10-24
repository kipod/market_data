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

    def is_match_bbo(self, order, bbo) -> bool:
        self.update_gen_bbo(order)
        delta = bbo.t2 - order.t2
        if delta > MAX_LATENCY_TIME:
            return False

        return self.gen_bbo == bbo

        # for debug
        # if self.gen_bbo == bbo:
        #     if delta > 10**9:
        #         return True
        #     return True
        # return False

    @staticmethod
    def is_matched_trade(order, trade) -> bool:
        delta = trade.t2 - order.t2
        if delta > MAX_LATENCY_TIME:
            return False
        return trade == order

    def find_matched_bbo(self, bbo):
        try:
            if self.gen_bbo is None:
                return None
            else:
                self.prev_gen_bbo = copy(self.gen_bbo)
            return self.find_match_message(bbo, self.is_match_bbo)
        finally:
            self.gen_bbo = bbo

    def find_matched_trade(self, trade):
        return self.find_match_message(trade, self.is_matched_trade)

    def find_match_message(self, quote, is_match):
        # remove old messages from queue
        while self.__messages:
            t2 = self.__messages[0].t2
            if t2 <= self.__last_matched_message_t2 or abs(t2 - quote.t2) > MAX_LATENCY_TIME:
                self.__messages.popleft()
            else:
                break

        # search in queue
        for order in self.__messages:
            if order.t2 > quote.t2:
                return None
            if is_match(order, quote):
                self.__last_matched_message_t2 = order.t2
                return order

        for order in self.next_message_from_file:
            if order.t2 > quote.t2:
                break
            if is_match(order, quote):
                self.__last_matched_message_t2 = order.t2
                return order
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
        if order_id in self.orders:
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
