from datetime import datetime, timezone, time, timedelta

DATA_SIZE = 8 + 8 + 4 + (4 * 4)

MAX_LATENCY_TIME = 10 * 1000 * 1000

ONE_SEC_IN_NANOSECOND = 1000 * 1000 * 1000

TIME_ZONE = timezone(timedelta(hours=-4))
# TIME_ZONE = timezone.utc

# SELECTED_SYMBOL_IDS = (222, )
SELECTED_SYMBOL_IDS = None


def time_from_timestamp(timestamp: int, without_timezone=False) -> datetime:
    return datetime.fromtimestamp(timestamp // ONE_SEC_IN_NANOSECOND, timezone.utc if without_timezone else TIME_ZONE)


def str_time_from_timestamp(timestamp: int, without_timezone=False) -> str:
    dt = time_from_timestamp(timestamp, without_timezone)
    s = dt.strftime('%H:%M:%S')
    s += '.' + str(int(timestamp % ONE_SEC_IN_NANOSECOND)).zfill(9)
    return s


def time_in_seconds(t: time):
    return t.second + t.minute*60 + t.hour*60*60
