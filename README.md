# CoinKlineDemo

## Overview

`CoinKlineDemo` is a Python project designed to interact with cryptocurrency exchanges, manage data, and perform tasks such as querying databases and collecting data. The project is structured into several modules to handle different functionalities like REST API interactions, database management, and task scheduling.

## Project Structure

- **build/**: Contains build-related files (if applicable).

- **config/**: Configuration files for the project.

- **data/**: Directory for storing data files.

- **log/**: Directory for log files.

- **script/**: Custom scripts for the project.

- src/

  : Source code directory.

  - core/

    : Core functionality of the project.

    - `__init__.py`: Initializes the core module.

    - `constant.py`: Defines constants used across the project.

    - `exception.py`: Custom exceptions for error handling.

    - `exchange.py`: Handles interactions with cryptocurrency exchanges.

    - `logs.py`: Logging utilities.

    - `proxy.py`: Proxy configuration and management.

    - databases/

      : Database-related modules.

      - `__init__.py`: Initializes the databases module.
      - `clickhouse.py`: ClickHouse database integration.
      - `sqlit.py`: SQLite database integration.

    - exchanges/

      : Exchange-specific REST API implementations.

      - rest/

        : REST API modules.

        - `__init__.py`: Initializes the REST module.
        - `binance_rest.py`: Binance REST API implementation.
        - `okx_rest.py`: OKX REST API implementation.

    - init/

      : Initialization modules for exchanges.

      - `__init__.py`: Initializes the init module.
      - `binance.py`: Binance exchange initialization.
      - `endpoint_config.py`: Endpoint configuration for exchanges.
      - `okx.py`: OKX exchange initialization.

    - models/

      : Data models for the project.

      - `__init__.py`: Initializes the models module.
      - `base_model.py`: Base model definitions.
      - `types-cpython-311-x86_64-linux-gnu.so`: Compiled type definitions.
      - `types.pyx`: Cython type definitions.

    - tasks/

      : Task-related modules.

      - `__init__.py`: Initializes the tasks module.
      - `data_collection.py`: Data collection tasks.
      - `query_database_task.py`: Database query tasks.
      - `main.py`: Main task execution script.

- **.gitignore**: Git ignore file for excluding files from version control.

- **setup.py**: Setup script for installing the project and its dependencies.

## Prerequisites

- Python 3.11
- Dependencies listed in `setup.py`

## Usage

1. Configure the project by editing files in the `config/` directory as needed.

2. Run the main script to start the application:

   ```bash
   python src/core/tasks/main.py
   
   ● list-symbols:
   python main.py list-symbols
   # ['BTC-USDT', 'ETH-USDT', 'ETHUSDT', 'BTCUSDT']
   
   ● latest --exchange EXCHANGE --symbol SYMBOL
   python main.py latest --exchange binance --symbol BTCUSDT
   # exchange   symbol                       open  ...                      close                 volume   timestamp
   # binance  BTCUSDT  108472.300000000000000000  ...  108482.300000000000000000  89.445000000000000000  1748512800
   
   ● range --exchange EXCHANGE --symbol SYMBOL --from FROM_TIMESTAMP --to TO_TIMESTAMP
   python main.py range --exchange binance --symbol BTCUSDT --from 1748499000 --to 1748499060
   # exchange   symbol                       open  ...                      close                 volume   timestamp
   # 0  binance  BTCUSDT  107653.500000000000000000  ...  107636.400000000000000000  53.166000000000000000  1748499000
   # 1  binance  BTCUSDT  107636.400000000000000000  ...  107644.500000000000000000  63.203000000000000000  1748499060
   ```

3. Logs will be generated in the `log/` directory, and data will be stored in the `data/` directory.

## Contributing

Feel free to submit issues or pull requests to improve the project. Ensure to follow the coding standards and test your changes before submitting.

## License

This project is licensed under the MIT License. See the LICENSE file for details.