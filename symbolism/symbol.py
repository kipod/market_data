class Symbol(object):

    def __init__(self, index: int, complete_symbol: str, listed: str,
                 is_etf: bool, rnd_lot: int, is_test: bool, sec_type: str,
                 price_digits: int, contract_mult: int, last_close: float,
                 volume: int, shares_out: float):
        self.id = index
        self.price_digits = price_digits
        self.sec_type = sec_type
        self.contract_multiplier = contract_mult
        self.name = complete_symbol
        self.listed = listed
        self.is_etf = is_etf
        self.rnd_lot = rnd_lot
        self.is_test = is_test
        self.last_close = last_close
        self.volume = volume
        self.shares_out = shares_out

    def __repr__(self):
        return self.name
