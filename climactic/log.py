#! /usr/bin/env python
"""
"""
import os
import sys
import logging
from colorlog import ColoredFormatter


TRACE = 5
logging.addLevelName(TRACE, 'TRACE')

def trace(self, message, *args, **kws):
    self.log(TRACE, message, *args, **kws)


logging.Logger.trace = trace
logging.TRACE = TRACE


class ClimacticFormatter(ColoredFormatter):
    """
    """


def init_interactive_logging(level=logging.DEBUG):
    """
    Initialized the 'climactic' parent logger.

    In general, a library should not initialize/configure
    logging. This method is only to be called by the
    climactic command-line utility.

    :param level: a logging level from py:mod:`logging`
    """
    if level == logging.CRITICAL:
        devnull = open(os.devnull, 'w')
        sys.stdout, sys.stderr = devnull, devnull

    climactic_logger = logging.getLogger("climactic")
    climactic_logger.handlers.clear()
    handler = logging.StreamHandler()

    formatter = ClimacticFormatter(
        "%(log_color)s%(levelname)-8s%(reset)s "
        "%(message_log_color)s%(message)s",
        datefmt=None,
        reset=True,
        log_colors={
            'TRACE': 'bold_white,bg_purple',
            'DEBUG': 'bold_white,bg_cyan',
            'INFO': 'bold_green',
            'WARNING': 'bold_yellow',
            'ERROR': 'bold_red',
            'CRITICAL': 'bold_white,bg_red',
        },
        secondary_log_colors={
            'message': {
                'TRACE': 'purple',
                'DEBUG': 'cyan',
                'ERROR': 'red'
            }
        },
        style='%'
    )

    handler.setFormatter(formatter)

    climactic_logger.addHandler(handler)
    climactic_logger.setLevel(level)

    return climactic_logger
