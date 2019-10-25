import contextlib
from urllib.request import build_opener

from .symbol import Symbol

opener = build_opener()


class SymbolList(object):
    """
    as @url u can us:
    http://symbols.ath/fullactive_20190927.txt
    """
    def __init__(self, url: str):
        self.symbols = list()
        index = 0
        with contextlib.closing(opener.open(url)) as f:
            for line in f.readlines():  # files are iterable
                line = line.strip().decode('utf-8')
                parts = line.split(',')
                complete_symbol = parts[0].strip()
                sec_type = parts[1].strip()
                listed = parts[2].strip()
                price_digits = int(parts[3].strip())
                contract_mult = int(parts[4].strip())
                is_etf = True if parts[5].strip().upper() == 'Y' else False
                rnd_lot = int(parts[6].strip())
                is_test = True if parts[7].strip().upper() == 'Y' else False
                shares_out = 0.0
                if len(parts) > 11:
                    shares_out = float(parts[11].strip())
                last_close = float(parts[9].strip())
                volume = int(parts[10].strip())
                self.symbols.append(Symbol(index, complete_symbol, listed, is_etf, rnd_lot, is_test,
                                           sec_type, price_digits, contract_mult, last_close, volume, shares_out))
                index += 1

    def __len__(self):
        return len(self.symbols)

    def __getitem__(self, item):
        if isinstance(item, int):
            return self.symbols[item]
        if isinstance(item, str):
            for symbol in self.symbols:
                if symbol.name.upper() == item.upper():
                    return symbol
        return None

    def __repr__(self):
        return '~{} symbols~'.format(len(self.symbols))
