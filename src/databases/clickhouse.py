import pandas as pd
import clickhouse_connect

from contextlib import asynccontextmanager
from clickhouse_connect.driver import AsyncClient
from config import DEFAULT_CLICKHOUSE_PARAM
from core.logs import init_logger

LOGGER = init_logger('ClickHouseClient')


class ClickHouseClient:
    def __init__(
            self,
            host: str,
            port: int,
            username: str,
            password: str
    ):
        self.host = host
        self.port = port
        self.username = username
        self.password = password

    @asynccontextmanager
    async def client_generator(self) -> AsyncClient:
        yield await clickhouse_connect.get_async_client(
            host=self.host,
            port=self.port,
            username=self.username,
            password=self.password
        )

    async def insert_dataframe(self, df: pd.DataFrame, table_name: str):
        async with self.client_generator() as client:
            try:
                return await client.insert_df(df=df, table=table_name)
            except Exception as e:
                LOGGER.error(f"Failed to insert DataFrame into {table_name}: {str(e)}")
                raise

    async def query_dataframe(self, sql: str) -> pd.DataFrame:
        try:
            async with self.client_generator() as client:
                return await client.query_df(sql)
        except Exception as e:
            LOGGER.error(f"Query DataFrame failed: {sql} {str(e)}")
            raise


default_click: ClickHouseClient = ClickHouseClient(**DEFAULT_CLICKHOUSE_PARAM)
