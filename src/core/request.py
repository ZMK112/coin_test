import httpx

from typing import Optional
from tenacity import retry, stop_after_attempt, wait_exponential
from .logs import init_logger

LOGGER = init_logger('RequestApi')


class RequestApi:
    def __init__(self, use_proxy: bool = True):
        self.use_proxy = use_proxy

    @property
    def proxies(self):
        return 'http://192.168.4.141:10869'

    @property
    def headers(self):
        return {
            "Content-Type": 'application/json',
            'Connection': 'keep-alive',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept': '*/*'
        }

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10), reraise=True)
    async def get_request(
            self,
            url: str,
            param: Optional[dict] = None,
            proxy: Optional[str] = None,
            headers: Optional[dict] = None,
            time_out: int = 10
    ):
        headers = headers or self.headers
        proxy = proxy or self.proxies

        async with httpx.AsyncClient(timeout=time_out, proxy=proxy) as client:
            try:
                response = await client.get(url, params=param, headers=headers)
                return await self._handle_response(response)
            except ValueError:
                LOGGER.error(f'Invalid Response:{url},{response.text}')
                raise

    @staticmethod
    async def _handle_response(response):
        status_code = response.status_code
        if status_code != 200:
            LOGGER.error(
                f"Status code {status_code} for URL {response.url},"
                f" Headers: {response.headers}"
            )
        if status_code == 429:
            LOGGER.error(f"Encountered a rate limit for address:{response.url}")
        response.raise_for_status()
        return response.text

    async def request(
            self,
            url: str,
            param: Optional[dict] = None,
            proxy: Optional[str] = None,
            headers: Optional[dict] = None,
            time_out: int = 10,
            method: str = 'GET'
    ):
        LOGGER.debug(f'Request {url}')
        return await self.get_request(url, param, proxy, headers, time_out)