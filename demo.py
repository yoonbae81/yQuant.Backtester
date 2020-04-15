import json
from multiprocessing import cpu_count
from types import SimpleNamespace

import backtester

CONFIG = {
    'initial_cash':
        100_000,
    'fetcher': {
        'ticks_path': 'ticks/',
    },
    'broker': {
        'ledger_dir': 'ledger/',
        'slippage_stdev': 0.7,
    },
    'analyzer': {
        'workers': max(1, cpu_count() - 1),
    },
    'files': {
        'logging': 'config/logging.json',
        'symbol': 'config/symbol.json',
        'market': 'config/market.json',
    }
}


def calc_quantity_to_buy(initial_cash, current_cash, holding, stock):
    return 1


def calc_quantity_to_sell(holding, stock):
    return 1


def calc_stoploss(stock):
    return 1


strategy = SimpleNamespace(
    calc_quantity_to_buy=calc_quantity_to_buy,
    calc_quantity_to_sell=calc_quantity_to_sell,
    calc_stoploss=calc_stoploss)

if __name__ == '__main__':
    for key, filepath in CONFIG['files'].items():
        with open(filepath, 'rt') as f:
            CONFIG[key] = json.load(f)

    backtester.run(CONFIG, strategy)
