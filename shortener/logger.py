"""
Logger functions
"""
import os
from datetime import datetime


def log(level, msg, *args, **kwargs):
    """
    Log message

    Args:
        level: log level
        msg: log message
        args: additional messages
        kwargs: additional messages
    """
    msg = str(msg)
    for arg in args:
        msg += '\n' + str(arg)
    for value in kwargs.values():
        msg += '\n' + str(value)

    log_data = {
        'level': level,
        'msg': str(msg) + ' ',
        'timestamp': datetime.utcnow().timestamp(),
    }

    if os.environ.get('FLASK_DEBUG', 0) == '1':
        print(f'{level}: {msg}')

    return log_data


def debug(msg, *args, **kwargs):
    log('debug', msg, *args, **kwargs)


def info(msg, *args, **kwargs):
    log('info', msg, *args, **kwargs)


def warning(msg, *args, **kwargs):
    log('warning', msg, *args, **kwargs)


def error(msg, *args, **kwargs):
    log('error', msg, *args, **kwargs)


def critical(msg, *args, **kwargs):
    log('critical', msg, *args, **kwargs)
