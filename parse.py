import argparse
import datetime
from market_data import BboMessages, MarketMessages, TradeMessages
from statistic import Output as Stat, DEFAULT_INTERVAL_SECONDS
from market_data.common import str_time_from_timestamp, SELECTED_SYMBOL_IDS

DEFAULT_MARKET_FILE = r'S:\temp\md\short\market_ARCA__2019_10_15-30.csv.bin'
DEFAULT_CQS_FILE = r'S:\temp\md\short\CQS_ARCA_P__2019_10_15-30.csv.bin'
DEFAULT_CTS_FILE = r'S:\temp\md\short\CTS_ARCA__2019_10_15-30.csv.bin'

# DEFAULT_MARKET_FILE = r'S:\temp\md\spy\market_ARCA__2019_10_15-30.csv.bin'
# DEFAULT_CQS_FILE = r'S:\temp\md\spy\CQS_ARCA_P__2019_10_15-30.csv.bin'
# DEFAULT_CTS_FILE = r'S:\temp\md\spy\CTS_ARCA__2019_10_15-30.csv.bin'
DEFAULT_OUT_FILE = 'output.csv'

g_interval = DEFAULT_INTERVAL_SECONDS


def main():
    parser = argparse.ArgumentParser(description='Market data parser.')
    parser.add_argument('--market', help='market data file', required=True)
    parser.add_argument('--CQS', help='CQS data file', default=None)
    parser.add_argument('--CTS', help='CTS data file', default=None)
    parser.add_argument('--out', help='path to output file', default=DEFAULT_OUT_FILE)
    parser.add_argument('--interval', help='statistic interval in second', default=None)

    args = parser.parse_args()
    if args.interval:
        global g_interval
        g_interval = int(args.interval)
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


class MatchCount(object):
    def __init__(self):
        self.quote_message_count = 1
        self.quote_matched_count = 0
        self.quote_not_matched_count = 0


def parse_market_vs_quotes(quote_src, output_file, find_matched):
    with Stat(output_file, g_interval) as stat:
        quote_message_count = 0
        quote_matched_count = 0
        quote_not_matched_count = 0
        max_delta = 0
        # print('Symbols:')
        symbol_ids = {}
        for quote_data in quote_src.get_next_message():
            if SELECTED_SYMBOL_IDS and quote_data.symbol_id not in SELECTED_SYMBOL_IDS:
                continue
            if quote_data.symbol_id not in symbol_ids:
                symbol_ids[quote_data.symbol_id] = MatchCount()
                # print('\t', quote_data.symbol_id)
            else:
                symbol_ids[quote_data.symbol_id].quote_message_count += 1
            quote_message_count += 1
            msg = find_matched(quote_data)
            if msg is not None:
                quote_matched_count += 1
                symbol_ids[quote_data.symbol_id].quote_matched_count += 1
                stat.add_stats(msg.t2, quote_data.t2)
                delta = quote_data.t2 - msg.t2
                if delta > max_delta:
                    max_delta = delta
            else:
                quote_not_matched_count += 1
                symbol_ids[quote_data.symbol_id].quote_not_matched_count += 1
        print('from {} quote messages'.format(quote_message_count))
        print('\t matched: {} ='.format(quote_matched_count),
              '{0:.0%}'.format(quote_matched_count / quote_message_count if quote_message_count else 0))
        print('max latency: {}'.format(str_time_from_timestamp(max_delta, True)))
        # By symbols
        print('By symbols')
        for sid in symbol_ids:
            print('Symbol:', sid)
            print('\tfrom {} quote messages'.format(symbol_ids[sid].quote_message_count))
            print('\t\t matched: {} ='.format(symbol_ids[sid].quote_matched_count),
                  '{0:.0%}'.format(symbol_ids[sid].quote_matched_count / symbol_ids[sid].quote_message_count
                                   if symbol_ids[sid].quote_message_count else 0))

        if [s for s in symbol_ids if symbol_ids[s].quote_matched_count < symbol_ids[s].quote_message_count // 2]:
            print('Symbols with matching < 50%:')
            for sid in [s for s in symbol_ids if
                        symbol_ids[s].quote_matched_count <= symbol_ids[s].quote_message_count // 2]:
                print('\t', sid)
            print('Symbols with matching > 50%:')
            for sid in [s for s in symbol_ids if
                        symbol_ids[s].quote_matched_count > symbol_ids[s].quote_message_count // 2]:
                print('\t', sid)

        if [s for s in symbol_ids if symbol_ids[s].quote_matched_count < int(symbol_ids[s].quote_message_count * 0.6)]:
            print('Symbols with matching > 60%:')
            for sid in [s for s in symbol_ids if
                        symbol_ids[s].quote_matched_count > int(symbol_ids[s].quote_message_count * 0.6)]:
                print('\t', sid)

        print('Symbols with matching > 70%:')
        for sid in [s for s in symbol_ids if
                    symbol_ids[s].quote_matched_count > int(symbol_ids[s].quote_message_count * 0.7)]:
            print('\t', sid)


if __name__ == '__main__':
    start_time = datetime.datetime.now()
    main()
    print('Lead time:', datetime.datetime.now() - start_time)
