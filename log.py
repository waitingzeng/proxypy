import os
import os.path as osp
from functools import partial


_PATH_PREFIX = '/var/log/'
import logging
import logging.config
from logging import _levelNames, getLogger
from logging.handlers import RotatingFileHandler
FORMAT = "<%(levelname)s> <%(name)s:%(filename)s:%(lineno)d:%(funcName)s> <%(process)d:%(threadName)s>%(asctime)-8s] %(message)s"
#FORMAT = "<%(levelname)s> <%(name)s> <%(process)d:%(threadName)s>%(asctime)-8s] %(message)s"


import logging

# format constant
SIMPLE_FORMAT = "%(message)s"
RECORD_FORMAT = "%(levelname)s: [%(asctime)s][%(filename)s:%(lineno)d][%(process)d:%(threadName)s][%(name)s] %(message)s"
COLOR_FORMAT = {
    'DEBUG'  : "\033[1;34m%(levelname)s\033[0m: [%(asctime)s][%(filename)s:%(lineno)d][%(process)d:%(threadName)s][%(name)s] %(message)s",
    'INFO'   : "\033[1;32m%(levelname)s\033[0m: [%(asctime)s][%(filename)s:%(lineno)d][%(process)d:%(threadName)s][%(name)s] %(message)s",
    'WARNING': "\033[1;33m%(levelname)s\033[0m: [%(asctime)s][%(filename)s:%(lineno)d][%(process)d:%(threadName)s][%(name)s] %(message)s",
    'ERROR'  : "\033[1;31m%(levelname)s\033[0m: [%(asctime)s][%(filename)s:%(lineno)d][%(process)d:%(threadName)s][%(name)s] %(message)s",
}
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

class ColorFormatter(logging.Formatter):
    def __init__(self, fmt=RECORD_FORMAT, datefmt=DATE_FORMAT):
        logging.Formatter.__init__(self, fmt, datefmt)

    def format(self, record):
        self._fmt = COLOR_FORMAT[record.levelname]
        return logging.Formatter.format(self, record)

class BasicFormatter(logging.Formatter):
    def __init__(self, fmt=RECORD_FORMAT, datefmt=DATE_FORMAT):
        logging.Formatter.__init__(self, fmt, datefmt)

    def format(self, record):
        return logging.Formatter.format(self, record)

class SimpleFormatter(logging.Formatter):
    def __init__(self, fmt=SIMPLE_FORMAT, datefmt=DATE_FORMAT):
        logging.Formatter.__init__(self, fmt, datefmt)

log_data = {}

class ContextFilter(logging.Filter):
    def filter(self, record):
        for k, v in log_data.items():
            setattr(record, k, v)
        return record


def get_logging_config(name, open_debug=False, loglevel=logging.INFO, **kwargs):
    log_file_name = '/var/log/%s.log' % name
    if not isinstance(loglevel, basestring):
        loglevel = logging._levelNames[loglevel]
    loglevel = loglevel.upper()
    log_data['name'] = name
    config = {
        'version': 1,
        'disable_existing_loggers': True,
        'formatters': {
            'color': {
                '()': ColorFormatter,
            },
            'basic': {
                '()': BasicFormatter,
            },
        },
        'filters': {
            'context': {
                '()': ContextFilter,
            }
        },
        'handlers': {
            'local_debug': {
                'level': 'DEBUG',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': log_file_name,
                'maxBytes': '50000000',
                'backupCount': 10,
                'formatter': 'basic',
                'filters': ['context'],
            },
            'std_debug': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'color',
                'filters': ['context'],
            },
        },
        'loggers': {
            '': {
                'level': loglevel,
                'handlers': ['std_debug', 'local_debug'] if open_debug else ['local_debug'],
                'propagate': False,
            },
        },
    }

    log_handlers = kwargs.pop('log_handlers', [])
    for log_handler in log_handlers:
        config['loggers'][log_handler] = config['loggers']['']
    return config

def open_log(name, loglevel=logging.DEBUG, **kwargs):
    config = get_logging_config(name, loglevel=loglevel, **kwargs)
    logging.config.dictConfig(config)

    return logging


def open_debug(name, loglevel=logging.DEBUG, **kwargs):
    logging.config.dictConfig(get_logging_config(name, True, loglevel=loglevel, **kwargs))
    return logging

