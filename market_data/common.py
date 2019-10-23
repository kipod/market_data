from datetime import datetime, timezone, time

DATA_SIZE = 8 + 8 + 4 + (4 * 4)

MAX_LATENCY_TIME = 20 * 1000 * 1000

ONE_SEC_IN_NANOSECOND = 1000 * 1000 * 1000


def time_from_timestamp(timestamp: int) -> datetime:
    return datetime.fromtimestamp(timestamp // ONE_SEC_IN_NANOSECOND, timezone.utc)


def str_time_from_timestamp(timestamp: int) -> str:
    dt = time_from_timestamp(timestamp)
    s = dt.strftime('%H:%M:%S')
    s += '.' + str(int(timestamp % ONE_SEC_IN_NANOSECOND)).zfill(9)
    return s


def time_in_seconds(t: time):
    return t.second + t.minute*60 + t.hour*60*60
