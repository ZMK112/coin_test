CREATE TABLE coin.binance_klines
(
    symbol String,
    exchange String,
    dtype String,
    freq String,
    open_time UInt64,
    open Decimal(38, 18),
    high Decimal(38, 18),
    low Decimal(38, 18),
    close Decimal(38, 18),
    volume Decimal(38, 18),
    close_time UInt64,
    quote_volume Decimal(38, 18),
    trades_cnt UInt64,
    taker_buy_base_volume Decimal(38, 18),
    taker_buy_quote_volume Decimal(38, 18),
    reversed Nullable(String) DEFAULT ''
)
ENGINE = MergeTree()
primary key (open_time,symbol,exchange)
PARTITION BY toYYYYMM(fromUnixTimestamp64Milli(open_time))
ORDER BY (open_time,symbol,exchange)
SETTINGS index_granularity = 8192;

CREATE TABLE coin.okx_klines
(
    symbol String,
    exchange String,
    dtype String,
    freq String,
    open_time UInt64,
    open Decimal(38, 18),
    high Decimal(38, 18),
    low Decimal(38, 18),
    close Decimal(38, 18),
    volume Decimal(38, 18),
    vol_ccy Decimal(38, 18),
    vol_ccy_quote Decimal(38, 18)
)
ENGINE = MergeTree()
primary key (open_time,symbol,exchange)
PARTITION BY toYYYYMM(fromUnixTimestamp64Milli(open_time))
ORDER BY (open_time,symbol,exchange)
SETTINGS index_granularity = 8192;


CREATE TABLE coin.klines
(
    exchange String,
    symbol String,
    open_time UInt64,
    open Decimal(38, 18),
    high Decimal(38, 18),
    low Decimal(38, 18),
    close Decimal(38, 18),
    volume Decimal(38, 18),
    timestamp UInt64 MATERIALIZED open_time / 1000
)
ENGINE = MergeTree()
primary key (open_time,symbol,exchange)
PARTITION BY toYYYYMM(fromUnixTimestamp64Milli(open_time))
ORDER BY (open_time,symbol,exchange)
SETTINGS index_granularity = 8192;