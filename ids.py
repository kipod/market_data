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
    # parser.parse_args(['-h'])
    args = parser.parse_args()
    try:
        datetime_object = datetime.strptime(args.date, '%d.%m.%Y')
    except ValueError as e:
        print('Wrong date format:', e)
        return
    url = datetime_object.strftime('http://symbols.ath/fullactive_%Y%m%d.txt')
    symbol_list = SymbolList(url)
    l_arca = [s for s in symbol_list if s.listed == 'P']
    for v in [s.id for s in l_arca if MIN_VOLUME < s.volume < MAX_VOLUME and not s.is_test and s.is_etf]:
        print(v)


if __name__ == '__main__':
    main()
