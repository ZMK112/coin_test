import sys
import click
import asyncio

from pathlib import Path

sys.path.append(Path(__file__).parent.parent.as_posix())
from tasks.query_database_task import query_obj


@click.group(invoke_without_command=True)
def main():
    pass
    # click.echo('Start kline task task')


@main.command(name='start_kline')
def start_kline():
    from tasks.data_collection import data_collector
    asyncio.run(data_collector.run())


@main.command(name='list-symbols')
def list_symbols():
    data = asyncio.run(query_obj.list_symbols())
    click.echo(data)
    return data


@main.command(name='latest')
@click.option('--exchange', type=str)
@click.option('--symbol', type=str)
def latest_bar(exchange, symbol):
    data = asyncio.run(query_obj.latest_bar(exchange, symbol, 1))
    click.echo(data)
    return data


@main.command(name='range')
@click.option('--exchange', type=str)
@click.option('--symbol', type=str)
@click.option('--from', 'start', type=int, help='Unix timestamp in seconds')
@click.option('--to', 'end', type=int, help='Unix timestamp in seconds')
def query_bar(exchange, symbol, start, end):
    data = asyncio.run(query_obj.query_bar(symbol, exchange, start, end))
    click.echo(data)
    return data


if __name__ == '__main__':
    main()
