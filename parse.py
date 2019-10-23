import argparse
from market_data import BboMessages, MarketMessages
from statistic import Output as Stat

# DEFAULT_MARKET_FILE = r'S:\temp\md\short\market_ARCA__2019_10_15-30.csv.bin'
# DEFAULT_CQS_FILE = r'S:\temp\md\short\CQS_ARCA_P__2019_10_15-30.csv.bin'
# DEFAULT_CTS_FILE = r'S:\temp\md\short\CTS_ARCA__2019_10_15-30.csv.bin'


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
    with Stat() as stat:
        market = MarketMessages(file_market)
        bbo_src = BboMessages(file_cqs)
        bbo_message_count = 0
        bbo_matched_count = 0
        bbo_not_matched_count = 0
        for bbo_data in bbo_src.get_next_message():
            bbo_message_count += 1
            msg = market.find_match_message(bbo_data)
            if msg is not None:
                bbo_matched_count += 1
                stat.add_stats(msg.t2, bbo_data.t2)
            else:
                bbo_not_matched_count += 1
        print('from {} bbo messages'.format(bbo_message_count))
        print('\t matched: {} ='.format(bbo_matched_count), '{0:.0%}'.format(bbo_matched_count / bbo_message_count))


if __name__ == '__main__':
    main()
