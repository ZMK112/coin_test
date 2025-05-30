cimport cython
from decimal import Decimal


cdef extern from *:
    """
    #ifdef CYTHON_WITHOUT_ASSERTIONS
    #define _COMPILED_WITH_ASSERTIONS 0
    #else
    #define _COMPILED_WITH_ASSERTIONS 1
    #endif
    """
    cdef bint _COMPILED_WITH_ASSERTIONS
COMPILED_WITH_ASSERTIONS = _COMPILED_WITH_ASSERTIONS

cdef dict convert_none_values(d: dict, s: str):
    for key, value in d.items():
        if value is None:
            d[key] = s
    return d

cdef class Candle:
    cdef readonly str exchange
    cdef readonly str symbol
    cdef readonly double start
    cdef readonly double stop
    cdef readonly str interval
    cdef readonly object trades  # None or int
    cdef readonly object open
    cdef readonly object close
    cdef readonly object high
    cdef readonly object low
    cdef readonly object volume
    cdef readonly bint closed
    cdef readonly object timestamp  # None or float
    cdef readonly object raw  # dict or list
    cdef readonly object reserve1
    cdef readonly object reserve2

    def __init__(
            self,
            exchange,
            symbol,
            start,
            stop,
            interval,
            trades,
            open,
            close,
            high,
            low,
            volume,
            closed,
            timestamp,
            raw=None,
            reserve1=None,
            reserve2=None
    ):
        assert trades is None or isinstance(trades, int)
        assert isinstance(open, Decimal)
        assert isinstance(close, Decimal)
        assert isinstance(high, Decimal)
        assert isinstance(low, Decimal)
        assert isinstance(volume, Decimal)
        assert timestamp is None or isinstance(timestamp, (float, int))

        self.exchange = exchange
        self.symbol = symbol
        self.start = start
        self.stop = stop
        self.interval = interval
        self.trades = trades
        self.open = open
        self.close = close
        self.high = high
        self.low = low
        self.volume = volume
        self.closed = closed
        self.timestamp = timestamp
        self.raw = raw
        self.reserve1 = reserve1
        self.reserve2 = reserve2

    @staticmethod
    def from_dict(data: dict) -> Candle:
        return Candle(
            data['exchange'],
            data['symbol'],
            data['start'],
            data['stop'],
            data['interval'],
            data['trades'],
            Decimal(data['open']),
            Decimal(data['close']),
            Decimal(data['high']),
            Decimal(data['low']),
            Decimal(data['volume']),
            data['closed'],
            data['timestamp'],
        )

    cpdef dict to_dict(self, numeric_type=None, none_to=False):
        if numeric_type is None:
            data = {
                'exchange': self.exchange, 'symbol': self.symbol, 'start': self.start, 'stop': self.stop,
                'interval': self.interval, 'trades': self.trades, 'open': self.open, 'close': self.close,
                'high': self.high, 'low': self.low, 'volume': self.volume, 'closed': self.closed,
                'timestamp': self.timestamp
            }
        else:
            data = {
                'exchange': self.exchange, 'symbol': self.symbol, 'start': self.start, 'stop': self.stop,
                'interval': self.interval, 'trades': self.trades, 'open': numeric_type(self.open),
                'close': numeric_type(self.close), 'high': numeric_type(self.high), 'low': numeric_type(self.low),
                'volume': numeric_type(self.volume), 'closed': self.closed, 'timestamp': self.timestamp
            }
        return data if not none_to else convert_none_values(data, none_to)

    def __repr__(self):
        return (
            f"exchange: {self.exchange} symbol: {self.symbol} start: {self.start} stop: {self.stop} "
            f"interval: {self.interval} trades: {self.trades} open: {self.open} close: {self.close} "
            f"high: {self.high} low: {self.low} volume: {self.volume} closed: {self.closed} "
            f"timestamp: {self.timestamp} reserve1: {self.reserve1} reserve2: {self.reserve2}"
        )

    def __eq__(self, cmp):
        return (
                self.exchange == cmp.exchange and self.symbol == cmp.symbol and self.start == cmp.start
                and self.stop == cmp.stop and self.interval == cmp.interval and self.trades == cmp.trades
                and self.open == cmp.open and self.close == cmp.close and self.high == cmp.high
                and self.low == cmp.low and self.volume == cmp.volume and self.timestamp == cmp.timestamp
        )

    def __hash__(self):
        return hash(self.__repr__())
