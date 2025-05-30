from typing import Optional, List
from databases.clickhouse import ClickHouseClient, default_click


class QueryMinBar:
    def __init__(self, clickhouse: Optional[ClickHouseClient] = None, min_table: str = 'coin.klines'):
        self.min_table = min_table
        self.click = clickhouse or default_click

    async def list_symbols(self) -> List[str]:
        sql = 'select distinct symbol from %s' % self.min_table
        df = await self.click.query_dataframe(sql)
        return df['symbol'].tolist()

    async def latest_bar(self, exchange: str, symbol: str, limit: int = 1):
        sql = """
        select * except(open_time),timestamp from %s
        where symbol='%s' and exchange='%s' order by open_time desc limit %s
        """ % (self.min_table, symbol, exchange, limit)
        return await self.click.query_dataframe(sql)

    async def query_bar(self, symbol: str, exchange: str, start_time: int, end_time: int):
        if start_time > end_time:
            raise ValueError('Start time must be before end time')
        sql = """
        select * except(open_time),timestamp from %s 
        where symbol='%s' and exchange='%s' and timestamp >= %s and timestamp <= %s
        """ % (self.min_table, symbol, exchange, start_time, end_time)
        return await self.click.query_dataframe(sql)


query_obj: QueryMinBar = QueryMinBar()
