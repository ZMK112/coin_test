import asyncio
import pandas as pd

from dataclasses import asdict

from exchanges.okx import OKXCoin
from exchanges.binance import BinanceFutures

obj: BinanceFutures = BinanceFutures()
okx_obj: OKXCoin = OKXCoin()


def test_binance_rest():
    print(obj.api)


def test_binance_generate_minbar():
    bartime = obj.generate_bar_item('BTC-USDT', 'linear')
    print(bartime)


async def test_binance_query_minbar():
    bartime = obj.generate_bar_item('BTCUSDT', 'linear')
    print(bartime)
    data = await obj.query_minbar_worker('klines', bartime)
    print(data)


def test_split_time_ranges():
    data = obj.split_time_range(1748316819355, 1748403159355, 60000, 200)
    print(data)


async def test_symbol_candles():
    data = await obj.query_symbol_candles(
        'BTCUSDT',
        'linear', 1748316819355,
        1748420780000,
        '1m',
        200,
        'klines'
    )
    df = pd.DataFrame([asdict(d) for d in data])
    print(df)


async def test_clickhouse():
    ADV_PARAM = {
        "username": 'default',
        "host": '192.168.1.70',
        "port": 8124,
        "password": '1234567'
    }
    from databases.clickhouse import ClickHouseClient
    obj = ClickHouseClient(**ADV_PARAM)
    data = await obj.query_dataframe('select * from coin.bybit_coin_minbar_30s limit 2')
    print(data)


async def test_insert_clickhouse():
    ADV_PARAM = {
        "username": 'default',
        "host": '192.168.1.70',
        "port": 8124,
        "password": '1234567'
    }
    from databases.clickhouse import ClickHouseClient
    click = ClickHouseClient(**ADV_PARAM)
    data = await obj.query_symbol_candles(
        'BTCUSDT',
        'linear', 1748316819355,
        1748420780000,
        '1m',
        200,
        'klines'
    )
    df = pd.DataFrame([asdict(d) for d in data])
    await click.insert_dataframe(df, 'coin.binance_klines')


async def test_okx_candle():
    start, end = 1748499000000 - 1, 1748499060000
    # start, end = 1748416320000 - 1, 1748416380000
    data = await okx_obj.query_symbol_candles(
        'BTC-USDT',
        'linear',
        start,
        end,
        '1m',
        200,
    )
    date = [d.open_time for d in data]
    # df = pd.DataFrame([asdict(d) for d in data])
    print(date)


async def test_query():
    from tasks.query_database_task import query_obj
    data = await query_obj.query_bar('BTCUSDT', 'binance', 1748429880, 1748429880)
    print(data)

    symbol = await query_obj.list_symbols()
    print(symbol)


async def test_symbols():
    await obj.symbols_candles_task(freq='1m')


async def test_okx_symbols():
    await okx_obj.symbols_candles_task(freq='1m')


def tmp():
    asyncio.run(test_query())


if __name__ == '__main__':
    tmp()
