import os.path

from pathlib import Path
from config.db_conf import *

PROJECT_DIRECTORY = Path(__file__).parent.parent.as_posix()
LOG_DIRECTORY = os.path.join(PROJECT_DIRECTORY, 'log')
DATA_DIRECTORY = os.path.join(PROJECT_DIRECTORY, 'data')
CHROME_BUFFER_DIRECTORY = os.path.join(DATA_DIRECTORY, 'chrome_buffer')
CONFIG_DIRECTORY = os.path.join(PROJECT_DIRECTORY, 'hyperliquid/config')
