import uvloop
import asyncio

from typing import Optional
from concurrent.futures import ProcessPoolExecutor

from exchanges.okx import OKXCoin
from exchanges.binance import BinanceFutures
from core.logs import init_logger

LOGGER = init_logger('DataRestCollect')


class DataRestCollect:

    def __init__(self, kline_table: Optional[str] = None, filter_columns: bool = True):
        try:
            asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
        except Exception as e:
            LOGGER.error(f"Set uvloop failed: {e}")
        else:
            LOGGER.info("uvloop initialized successfully.")

        self.kline_table = kline_table
        self.filter_columns = filter_columns
        self._loop = None

    @property
    def event_loop(self):
        try:
            return asyncio.get_running_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            return loop

    @property
    def loop(self):
        if self._loop is None:
            self._loop = self.event_loop
        return self._loop

    async def binance_kline_task(self):
        task_obj: BinanceFutures = BinanceFutures(
            table=self.kline_table, filter_columns=self.filter_columns)
        await task_obj.symbols_candles_task()

    async def okx_kline_task(self):
        task_obj: OKXCoin = OKXCoin(
            table=self.kline_table, filter_columns=self.filter_columns)
        await task_obj.symbols_candles_task()

    @staticmethod
    def run_async_task(function):
        return asyncio.run(function())

    async def run(self):
        functions = [self.binance_kline_task, self.okx_kline_task]
        with ProcessPoolExecutor(max_workers=len(functions)) as pool:
            futures = [
                self.event_loop.run_in_executor(pool, self.run_async_task, f)
                for f in functions
            ]
            for future in asyncio.as_completed(futures):
                await future.result()


data_collector: DataRestCollect = DataRestCollect(kline_table='coin.klines')

if __name__ == '__main__':
    asyncio.run(data_collector.run())
