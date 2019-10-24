import argparse
from market_data import BboMessages, MarketMessages, TradeMessages
from statistic import Output as Stat
from market_data.common import str_time_from_timestamp

DEFAULT_MARKET_FILE = r'S:\temp\md\short\market_ARCA__2019_10_15-30.csv.bin'
DEFAULT_CQS_FILE = r'S:\temp\md\short\CQS_ARCA_P__2019_10_15-30.csv.bin'
DEFAULT_CTS_FILE = r'S:\temp\md\short\CTS_ARCA__2019_10_15-30.csv.bin'

# DEFAULT_MARKET_FILE = r'S:\temp\md\spy\market_ARCA__2019_10_15-30.csv.bin'
# DEFAULT_CQS_FILE = r'S:\temp\md\spy\CQS_ARCA_P__2019_10_15-30.csv.bin'
# DEFAULT_CTS_FILE = r'S:\temp\md\spy\CTS_ARCA__2019_10_15-30.csv.bin'
DEFAULT_OUT_FILE = 'output.csv'


def main():
    parser = argparse.ArgumentParser(description='Market data parser.')
    parser.add_argument('--market', help='market data file', default=DEFAULT_MARKET_FILE)
    parser.add_argument('--CQS', help='CQS data file', default=None)
    parser.add_argument('--CTS', help='CTS data file', default=None)
    parser.add_argument('--out', help='path to output file', default=DEFAULT_OUT_FILE)

    args = parser.parse_args()
    if args.market and args.CQS:
        parse_market_vs_bbo(args.market, args.CQS, args.out)
    elif args.market and args.CTS:
        parse_market_vs_trades(args.market, args.CTS, args.out)
    else:
        print('Wrong arguments')
        parser.print_usage()


def parse_market_vs_bbo(file_market, file_cqs, output_file):
    market_src = MarketMessages(file_market)
    parse_market_vs_quotes(BboMessages(file_cqs), output_file, market_src.find_matched_bbo)


def parse_market_vs_trades(file_market, file_trades, output_file):
    market_src = MarketMessages(file_market)
    parse_market_vs_quotes(TradeMessages(file_trades), output_file, market_src.find_matched_trade)


def parse_market_vs_quotes(quote_src, output_file, find_matched):
    with Stat(output_file) as stat:
        quote_message_count = 0
        quote_matched_count = 0
        quote_not_matched_count = 0
        max_delta = 0
        for quote_data in quote_src.get_next_message():
            quote_message_count += 1
            msg = find_matched(quote_data)
            if msg is not None:
                quote_matched_count += 1
                stat.add_stats(msg.t2, quote_data.t2)
                delta = quote_data.t2 - msg.t2
                if delta > max_delta:
                    max_delta = delta
            else:
                quote_not_matched_count += 1
        print('from {} quote messages'.format(quote_message_count))
        print('\t matched: {} ='.format(quote_matched_count),
              '{0:.0%}'.format(quote_matched_count / quote_message_count))
        print('max latency: {}'.format(str_time_from_timestamp(max_delta, True)))


if __name__ == '__main__':
    main()
