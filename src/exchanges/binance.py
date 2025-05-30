import asyncio
import pandas as pd

from asyncio import Queue
from dataclasses import asdict
from typing import Optional, List

# from models.types import Candle
from models import QueryItem, BinanceKlineRecord
from exchanges.rest import BinanceFuturesRest
from core.constant import BINANCE_FUTURES
from databases.clickhouse import ClickHouseClient, default_click
from core.logs import init_logger

LOGGER = init_logger('BinanceFutures')


class BinanceFutures(BinanceFuturesRest):
    exchange = BINANCE_FUTURES
    start_delay = 5
    request_limit = 200
    buffer_size = 20
    queue_size = 1000
    buffer_out_time = 120_000
    kline_endpoint = 'klines'
    default_freq = '1m'
    valid_candle_intervals: dict = {'1m': 1, '3m': 3, '1h': 60}

    def __init__(
            self,
            clickhouse: Optional[ClickHouseClient] = None,
            table: Optional[str] = None,
            filter_columns: bool = True
    ):
        super().__init__()
        self.click = clickhouse or default_click
        self.min_table = table or self.default_min_table
        self.filter_columns = filter_columns
        self._condition = asyncio.Condition()
        self._last_bar = {}
        self._breaking = False
        self._queue = None

    @property
    def queue(self):
        if self._queue is None:
            self._queue = Queue(maxsize=self.queue_size)
        return self._queue

    def get_last_bar(self, symbol: str):
        if symbol not in self._last_bar:
            self._last_bar[symbol] = self.first_bar_time
        return self._last_bar[symbol]

    @property
    def trading_symbols(self):
        return ['BTCUSDT', 'ETHUSDT']

    def _generate_query_items(
            self,
            symbol: str,
            dtype: str,
            start: int,
            end: int,
            bar_range: int,
            limit_cnt: int,
            freq: str
    ) -> List[QueryItem]:
        if freq not in self.valid_candle_intervals:
            raise ValueError(f"Invalid frequency: {freq}. Supported: {list(self.valid_candle_intervals.keys())}")
        if start >= end:
            raise ValueError("Start time must be before end time")
        ranges = self.split_time_range(start, end, bar_range, limit_cnt)
        return [QueryItem(symbol, dtype, freq, *r) for r in ranges]

    async def query_candle_worker(self, query_item: QueryItem, endpoint: str) -> List[BinanceKlineRecord]:
        msgs = await self.query_minbar_worker(endpoint, query_item)
        symbol, exchange, dtype, freq = (
            query_item.symbol,
            self.exchange,
            query_item.dtype,
            query_item.freq
        )
        return [BinanceKlineRecord(symbol, exchange, dtype, freq, *m) for m in msgs if m]

    async def query_symbol_candles(
            self,
            symbol: str,
            dtype: str,
            start: int,
            end: int,
            freq: str,
            limit_cnt: int,
            endpoint: str
    ) -> List[BinanceKlineRecord]:
        bar_range = self.valid_candle_intervals[freq] * 60_000
        query_items = self._generate_query_items(
            symbol=symbol,
            dtype=dtype,
            start=start,
            end=end,
            bar_range=bar_range,
            limit_cnt=limit_cnt,
            freq=freq
        )

        results = []
        for query_item in query_items:
            try:
                candle = await self.query_candle_worker(query_item, endpoint)
                results.extend(candle)
            except Exception as e:
                LOGGER.warning(f'Query {query_item} failed: {str(e)}')
        if results:
            results.sort(key=lambda x: x.close_time)
        return results

    async def symbol_candles_with_save(
            self,
            symbol: str,
            dtype: str,
            start: int,
            end: int,
            freq: str,
            limit_cnt: int = request_limit,
            endpoint: str = kline_endpoint,
    ):
        current_minute = self.current_minute
        candles = await self.query_symbol_candles(
            symbol=symbol,
            dtype=dtype,
            start=start,
            end=end,
            freq=freq,
            limit_cnt=limit_cnt,
            endpoint=endpoint
        )
        candles = [c for c in candles if c.close_time < current_minute]
        if not candles:
            return
        self._last_bar[symbol] = candles[-1].close_time
        async with self._condition:
            await self.queue.put(candles)
            self._condition.notify()

    async def flush_buffer(self):
        LOGGER.debug(f'Start flush buffer,the size of queue:{self.queue.qsize()}')
        records = []
        while not self.queue.empty():
            record = await self.queue.get()
            records.append(record)
        return records

    async def insert_records(self, records: List):
        records = [asdict(d) for r in records for d in r if r]
        df = pd.DataFrame(records)
        try:
            if self.filter_columns:
                df = df[self.base_columns]
            await self.click.insert_dataframe(df, self.min_table)
        except Exception as e:
            LOGGER.error(f"Insert records failed: {str(e)}")
        LOGGER.debug(f"Insert records successfully: {len(df)}")

    async def _watcher(self):
        await asyncio.sleep(self.start_delay)
        while not self._breaking:
            async with self._condition:
                await self._condition.wait_for(
                    lambda: (self.queue.qsize() >= self.buffer_size) or
                            (self.current_minute - min(self._last_bar.values()) >= self.buffer_out_time
                             and not self.queue.empty())
                )
                records = await self.flush_buffer()
            if records:
                await self.insert_records(records)

    async def symbol_candles_worker(self, symbol: str, dtype: str, freq: str):
        bar_range = self.valid_candle_intervals[freq] * 60_000
        while not self._breaking:
            last_tick = self.get_last_bar(symbol)
            last_minute = self.last_minute
            delay_milliseconds = last_minute - last_tick
            if delay_milliseconds >= bar_range:
                await self.symbol_candles_with_save(
                    symbol=symbol,
                    dtype=dtype,
                    start=last_tick + 1,
                    end=last_minute - 1,
                    freq=freq,
                )
            LOGGER.debug(
                f"{symbol}-{dtype}-{self.exchange}-{freq}:{last_tick=}"
                f",delay:{delay_milliseconds} milliseconds"
            )
            await asyncio.sleep(2)

    async def symbols_candles_task(
            self,
            symbols: Optional[str] = None,
            dtype: str = 'linear',
            freq: str = default_freq,
    ):
        symbols = symbols or self.trading_symbols
        tasks = [self.symbol_candles_worker(s, dtype, freq) for s in symbols]
        tasks.append(self._watcher())
        await asyncio.gather(*tasks)
