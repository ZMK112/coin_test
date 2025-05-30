from decimal import Decimal
from dataclasses import dataclass


@dataclass
class QueryItem:
    symbol: str
    dtype: str
    freq: str
    open_time: int
    close_time: int


@dataclass
class BinanceKlineRecord:
    symbol: str
    exchange: str
    dtype: str
    freq: str
    open_time: int
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
    volume: Decimal
    close_time: int
    quote_volume: Decimal
    trades_cnt: int
    taker_buy_base_volume: Decimal
    taker_buy_quote_volume: Decimal
    reversed: str = ''


@dataclass
class OKXKlineRecord:
    symbol: str
    exchange: str
    dtype: str
    freq: str
    open_time: int
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
    volume: Decimal
    vol_ccy: Decimal
    vol_ccy_quote: Decimal

    def __post_init__(self):
        if isinstance(self.open_time, str):
            self.open_time = int(self.open_time)
