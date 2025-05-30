from enum import Enum


BINANCE = 'BINANCE'
BINANCE_US = 'BINANCE_US'
BINANCE_TR = 'BINANCE_TR'
BINANCE_FUTURES = 'binance'
# BINANCE_FUTURES = 'BINANCE_FUTURES'
BINANCE_DELIVERY = 'BINANCE_DELIVERY'
OKCOIN = 'OKCOIN'
# OKX = 'OKX'
OKX = 'okx'


# Market Data
L1_BOOK = 'l1_book'
L2_BOOK = 'l2_book'
L3_BOOK = 'l3_book'
TRADES = 'trades'
TICKER = 'ticker'
FUNDING = 'funding'
OPEN_INTEREST = 'open_interest'
LIQUIDATIONS = 'liquidations'
INDEX = 'index'
UNSUPPORTED = 'unsupported'
CANDLES = 'candles'

# Account Data / Authenticated Channels
ORDER_INFO = 'order_info'
FILLS = 'fills'
TRANSACTIONS = 'transactions'
BALANCES = 'balances'
POSITIONS = 'positions'
PLACE_ORDER = 'place_order'
CANCEL_ORDER = 'cancel_order'
ORDERS = 'orders'
ORDER_STATUS = 'order_status'
TRADE_HISTORY = 'trade_history'

BUY = 'buy'
SELL = 'sell'
BID = 'bid'
ASK = 'ask'
UND = 'undefined'
MAKER = 'maker'
TAKER = 'taker'
LONG = 'long'
SHORT = 'short'
BOTH = 'both'

LIMIT = 'limit'
MARKET = 'market'
STOP_LIMIT = 'stop-limit'
STOP_MARKET = 'stop-market'
MAKER_OR_CANCEL = 'maker-or-cancel'
FILL_OR_KILL = 'fill-or-kill'
IMMEDIATE_OR_CANCEL = 'immediate-or-cancel'
GOOD_TIL_CANCELED = 'good-til-canceled'
TRIGGER_LIMIT = 'trigger-limit'
TRIGGER_MARKET = 'trigger-market'
MARGIN_LIMIT = 'margin-limit'
MARGIN_MARKET = 'margin-market'

OPEN = 'open'
PENDING = 'pending'
FILLED = 'filled'
PARTIAL = 'partial'
CANCELLED = 'cancelled'
UNFILLED = 'unfilled'
EXPIRED = 'expired'
SUSPENDED = 'suspended'
FAILED = 'failed'
SUBMITTING = 'submitting'
CANCELLING = 'cancelling'
CLOSED = 'closed'

# Instrument Definitions
SWAP = 'swap'
CURRENCY = 'currency'
FUTURES = 'futures'
PERPETUAL = 'perpetual'
OPTION = 'option'
OPTION_COMBO = 'option_combo'
FUTURE_COMBO = 'future_combo'
SPOT = 'spot'
CALL = 'call'
PUT = 'put'
FX = 'fx'

# HTTP methods
GET = 'GET'
DELETE = 'DELETE'
POST = 'POST'

KEEPALIVE_TIMEOUT = 5 * 60

EXCHANGE_SUFFIX_MAP = {
    BINANCE: 'bn',
    BINANCE_FUTURES: 'bn',
    BINANCE_DELIVERY: 'bn',
    BINANCE_US: 'bn',
    BINANCE_TR: 'bn',
    OKX: 'ok',
    OKCOIN: 'ok',
}


class WSListenerState(Enum):
    INITIALISING = "Initialising"
    STREAMING = "Streaming"
    RECONNECTING = "Reconnecting"
    EXITING = "Exiting"
