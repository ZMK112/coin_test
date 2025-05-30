from yapic import json
from decimal import Decimal
from urllib.parse import urlencode

from models import QueryItem
from core.request import RequestApi
from core.exchange import RestExchange
from config import default_store_bar_tables
from exchanges.endpoint_config import BinanceRestPoint as RestPoint


class BinanceFuturesRest(RequestApi, RestExchange):
    @property
    def api(self):
        try:
            return RestPoint.get(self.__class__.__name__)['api']
        except (KeyError, TypeError):
            raise AttributeError(f"No API endpoint found for {self.__class__.__name__}")

    @property
    def default_min_table(self):
        return default_store_bar_tables.get(self.__class__.__name__)

    async def __request(self, url: str, **kwargs):
        query_string = urlencode(kwargs)
        data = await self.request(f'{url}?{query_string}')
        return json.loads(data, parse_float=Decimal)

    async def query_minbar_worker(self, endpoint: str, bar: QueryItem):
        """
        [
          [
            1499040000000,      // Open time
            "0.01634790",       // Open
            "0.80000000",       // High
            "0.01575800",       // Low
            "0.01577100",       // Close
            "148976.11427815",  // Volume
            1499644799999,      // Close time
            "2434.19055334",    // Quote asset volume
            308,                // Number of trades
            "1756.87402397",    // Taker buy base asset volume
            "28.46694368",      // Taker buy quote asset volume
            "17928899.62484339" // Ignore.
          ]
        ]
        """
        url = f'{self.api}{endpoint}'
        return await self.__request(
            url=url,
            symbol=bar.symbol,
            startTime=bar.open_time,
            endTime=bar.close_time,
            interval=bar.freq
        )
