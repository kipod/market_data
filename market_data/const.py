from datetime import datetime, timezone


DATA_SIZE = 8 + 8 + 4 + (4 * 4)

MAX_LATENCY_TIME = 20 * 1000 * 1000

ONE_SEC_IN_NANOSECOND = 1000 * 1000 * 1000


def str_time_from_timestamp(timestamp: int) -> str:
    dt = datetime.fromtimestamp(timestamp // ONE_SEC_IN_NANOSECOND, timezone.utc)
    s = dt.strftime('%H:%M:%S')
    s += '.' + str(int(timestamp % ONE_SEC_IN_NANOSECOND)).zfill(9)
    return s
