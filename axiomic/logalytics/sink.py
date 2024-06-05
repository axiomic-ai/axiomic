import atexit

import axiomic.logalytics.events as events


import axiomic.logalytics.console_log as console_log 
import axiomic.logalytics.stats_counter as stats_counter 

import axiomic.configure.default_config as default_config

STATS_COUNTER = stats_counter.StatsCounter()

def exit_handler():
    if STATS_COUNTER is not None:
        STATS_COUNTER.print_stats()

if default_config.console_config.enable:
    atexit.register(exit_handler)

HANDLERS = []

if default_config.console_config.enable:
    HANDLERS.append(console_log.ConsoleLog())
    HANDLERS.append(STATS_COUNTER)


def event_sink(event: events.Event):
    for handler in HANDLERS:
        handler.log_event(event)

def discover_config(message):
    event = events.Event('config', events.EventType.CONFIG_DISCOVER, {'message': message})
    event_sink(event)
    