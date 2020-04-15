import json
import logging
from threading import Thread
from multiprocessing import Manager, Process, Queue, Event

from . import analyzer
from . import broker
from . import fetcher


def run(config, strategy):
    logging.config.dictConfig(config['logging'])

    manager = Manager()
    cash = manager.Value(float, config['initial_cash'])
    quantity_dict = manager.dict()

    tick_queues = [Queue() for _ in range(config['analyzer']['workers'])]
    order_queue = Queue()
    log_queue = Queue()
    done = Event()

    threads = [
        Thread(target=log_daemon,
               name='Logger',
               args=('Analyzer', log_queue)),

        Thread(target=fetcher.run,
               name='Fetcher',
               args=(config['fetcher']['ticks_path'],
                     tick_queues,
                     done)),

        Thread(target=broker.run,
               name='Broker',
               args=(config,
                     cash,
                     quantity_dict,
                     order_queue,
                     done)),
    ]

    processes = []
    for i, tick_queue in enumerate(tick_queues, 1):
        p = Process(target=analyzer.run,
                    name=f'Analyzer{i}',
                    args=(config,
                          strategy,
                          cash,
                          quantity_dict,
                          tick_queue,
                          order_queue,
                          log_queue,
                          done))
        processes.append(p)

    [t.start() for t in threads]
    [p.start() for p in processes]
    [p.join() for p in processes]
    log_queue.put(None)
    [t.join() for t in threads]


def log_daemon(name, queue):
    while record := queue.get():
        logging.getLogger(name).handle(record)