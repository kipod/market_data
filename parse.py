import argparse
from market_data import BboMessages, MarketMessages

DEFAULT_MARKET_FILE = r'S:\temp\md\market_ARCA__2019_10_15-30.csv.bin'
DEFAULT_CQS_FILE = r'S:\temp\md\CQS_ARCA_P__2019_10_15-30.csv.bin'
DEFAULT_CTS_FILE = r'S:\temp\md\CTS_ARCA__2019_10_15-30.csv.bin'


def main():
    parser = argparse.ArgumentParser(description='Market data parser.')
    parser.add_argument('--market', help='market data file', default=DEFAULT_MARKET_FILE)
    parser.add_argument('--CQS', help='CQS data file', default=DEFAULT_CQS_FILE)
    parser.add_argument('--CTS', help='CTS data file', default=DEFAULT_CTS_FILE)

    args = parser.parse_args()
    if args.market and args.CQS:
        parse_market_vs_CQS(args.market, args.CQS)
    pass


def parse_market_vs_CQS(file_market, file_cqs):
    market = MarketMessages(file_market)
    bbo_src = BboMessages(file_cqs)
    for bbo_data in bbo_src.get_next_message():
        msg = market.find_match_message(bbo_data)
        if msg is not None:
            add_stats(msg.t2, bbo_data.t2)


def add_stats(market_time, quote_time):
    assert quote_time > market_time
    # TODO


if __name__ == '__main__':
    main()
