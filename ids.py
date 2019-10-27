#!/bin/python3
import argparse
from datetime import datetime
from symbolism import SymbolList

MIN_VOLUME = 200000
MAX_VOLUME = 300000


def main():
    parser = argparse.ArgumentParser(description='Market data parser.')
    required = parser.add_argument_group('required named arguments')
    required.add_argument('-d', '--date', help='date for symbol selector', required=True)
    parser.add_argument('-o', '--output', help='Output file name', default='stdout')
    parser.add_argument('-s', '--symbols', help='set of symbols', default=None)
    parser.add_argument('-n', '--show_names', action='store_true', help='show symbol names')
    parser.add_argument('-l', '--listed', help='Listed exchange code [PNZQ]', default='P')
    parser.add_argument('--max', help='Max volume', default=MAX_VOLUME, type=int)
    parser.add_argument('--min', help='Min volume', default=MIN_VOLUME, type=int)
    # parser.parse_args(['-h'])
    args = parser.parse_args()
    try:
        datetime_object = datetime.strptime(args.date, '%d.%m.%Y')
    except ValueError as e:
        print('Wrong date format:', e)
        return
    url = datetime_object.strftime('http://symbols.ath/fullactive_%Y%m%d.txt')
    user_symbols = args.symbols.split(';') if args.symbols else None
    symbol_list = SymbolList(url)
    l_exchange = [s for s in symbol_list if s.listed == args.listed]
    if user_symbols:
        l_exchange = [s for s in l_exchange if s.name in user_symbols]
    for v in [s.name if args.show_names else s.id \
         for s in l_exchange if args.min < s.volume < args.max and not s.is_test]:
        print(v)


if __name__ == '__main__':
    main()
