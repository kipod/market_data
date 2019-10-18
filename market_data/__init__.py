from .order import Order
from .trade import Trade
from .bbo import BBO
from .const import DATA_SIZE
from .bbo_messages import BboMessages
from .market_messages import MarketMessages

# MAX_COUNT = 100000


# def get_bbo_data(file_path):
#     bbo_src = BboMessages(file_path)
#     return bbo_src.get_next_message()
