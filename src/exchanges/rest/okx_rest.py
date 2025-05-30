from yapic import json
from decimal import Decimal
from urllib.parse import urlencode

from models import QueryItem
from core.request import RequestApi
from core.exchange import RestExchange
from config import default_store_bar_tables
from exchanges.endpoint_config import OKXRestPoint as RestPoint


class OKXRest(RequestApi, RestExchange):
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
        url = f'{url}?{urlencode(kwargs)}'
        data = await self.request(url)
        return json.loads(data, parse_float=Decimal)

    async def query_minbar_worker(self, endpoint: str, bar: QueryItem):
        """
        [
             [
                "1597026383085",           // Opening time of the candlestick, Unix timestamp format in milliseconds, e.g. 1597026383085
                "3.721",                   // Open price
                "3.743",                   // Highest price
                "3.677",                   // Lowest price
                "3.708",                   // Close price
                "8422410",                 // Trading volume If it is SPOT, the value is the quantity in base currency.
                "22698348.04828491",       // Trading volume If it is SPOT, the value is the quantity in quote currency.
                "12698348.04828491",       // Trading volume, the value is the quantity in quote currency e.g. The unit is USDT for BTC-USDT
                "0"                        // The state of candlesticks. 0: K line is uncompleted 1: K line is completed
            ],
            [
                "1597026383085",
                "3.731",
                "3.799",
                "3.494",
                "3.72",
                "24912403",
                "67632347.24399722",
                "37632347.24399722",
                "1"
            ]
        ]
        """
        url = f'{self.api}{endpoint}'
        return await self.__request(
            url=url,
            instId=bar.symbol,
            before=bar.open_time,
            after=bar.close_time,
            bar=bar.freq
        )
