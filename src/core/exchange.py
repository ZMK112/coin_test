import asyncio
import numpy as np

from typing import List, Optional, Tuple, Union
from datetime import datetime as dt, timezone, timedelta


class RestExchange:
    api: Union[str, List[str]]
    sandbox_api: Union[str, List[str]]
    rest_channels: Union[str, List[str]]
    history_start_hours: int = 24
    base_columns = ['exchange', 'symbol', 'open_time', 'open', 'high', 'low', 'close', 'volume']

    @property
    def today(self):
        now_time = dt.now()
        if now_time.strftime('%H:M:%S') >= '08:00:00':
            return now_time.strftime('%Y%m%d')
        return (now_time - timedelta(days=1)).strftime('%Y%m%d')

    @staticmethod
    def datetime_normalize(timestamp: Union[str, int, float, dt] = None) -> float:
        if timestamp is None:
            return dt.utcnow().timestamp()
        if isinstance(timestamp, (float, int)):
            return timestamp
        if isinstance(timestamp, dt):
            return timestamp.astimezone(timezone.utc).timestamp()
        if isinstance(timestamp, str):
            formats = ['%Y-%m-%d %H:%M:%S.%f', '%Y-%m-%d %H:%M:%S']
            for format_ in formats:
                try:
                    return dt.strptime(timestamp, format_).replace(tzinfo=timezone.utc).timestamp()
                except Exception:
                    pass
        raise ValueError(f'Timestamp is invalid: {timestamp}')

    def interval_normalize(self, start, end) -> Tuple[Optional[float], Optional[float]]:
        start = self.datetime_normalize(start)
        end = self.datetime_normalize(end)
        if start and start > end:
            raise ValueError('Start time must be less than or equal to end time')
        return start, end

    def datetime_millisecond(self, timestamp: Union[str, dt] = None) -> int:
        return int(self.datetime_normalize(timestamp) * 1000)

    @staticmethod
    def split_time_range(start: int, end: int, bar_range: int, limit_cnt: int):
        if end - start > limit_cnt * bar_range:
            time_ranges = []
            while start <= end:
                time_ranges.append(start)
                start += bar_range
            ranges = np.array_split(time_ranges, len(time_ranges) // limit_cnt)
            return [(r[0], r[-1]) for r in ranges]
        return [(start, end)]

    @property
    def minute_truncate(self):
        return dt.now().replace(second=0, microsecond=0)

    @property
    def first_bar_time(self):
        return self.datetime_millisecond(self.minute_truncate - timedelta(hours=self.history_start_hours))

    @property
    def last_minute(self):
        return self.datetime_millisecond(self.minute_truncate - timedelta(minutes=1))

    @property
    def current_minute(self):
        return self.datetime_millisecond(self.minute_truncate)
