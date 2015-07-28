#! /usr/bin/env python
"""
"""

__all__ = [
    'init_interactive_logging',
    'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'
]


import logging

import colorama
colorama.init()


DEBUG, INFO, WARNING, ERROR, CRITICAL = (
    logging.DEBUG,
    logging.INFO,
    logging.WARNING,
    logging.ERROR,
    logging.CRITICAL
)
TRACE = 5
logging.addLevelName(TRACE, 'TRACE')


BaseLogger = logging.getLoggerClass()


class ExtendedLogger(BaseLogger):

    """
    Adds extra features to logging.Logger:

    - trace()
    - colorization
    """

    def trace(self, msg, *args, **kwargs):
        """
        Log 'msg % args' with severity 'TRACE'.
        """
        if self.isEnabledFor(TRACE):
            self._log(TRACE, msg, args, **kwargs)


logging.setLoggerClass(ExtendedLogger)


class ColorTag(object):

    """
    """

    def __init__(self, color_collection):
        self.color_collection = color_collection

    def __format__(self, format_spec):
        format_spec = format_spec.upper()
        if format_spec.endswith("+"):
            format_spec = "LIGHT" + format_spec[:-1] + "_EX"
        return getattr(self.color_collection, format_spec)


class ColorLogRecord(logging.LogRecord):
    def __init__(self, name, level, pathname, lineno, msg, args, exc_info,
                 func=None, sinfo=None, **kwargs):
        self.FG = ColorTag(colorama.Fore)
        self.BG = ColorTag(colorama.Back)
        self.R = colorama.Style.RESET_ALL
        self.color_mappings = self.__dict__.copy()
        super().__init__(name, level, pathname, lineno, msg, args, exc_info,
                         func, sinfo, **kwargs)

    def getMessage(self):
        return self.msg.format(*self.args, **self.color_mappings)


logging.setLogRecordFactory(ColorLogRecord)


class PerLevelFormatter(logging.Formatter):

    """
    """

    def __init__(self, fmt=None, datefmt=None):
        self.format_by_level = {
            TRACE:    "{BG:magenta}{FG:white+} {levelname} {R}    "
                      "{FG:magenta+}{message}{R}",

            DEBUG:    "{BG:cyan}{FG:black+} {levelname} {R}    "
                      "{FG:cyan+}{message}{R}",

            INFO:     "{message}{R}",

            WARNING:  "{BG:yellow+}{FG:black+} {levelname} {R}  "
                      "{FG:yellow+}{message}{R}",

            ERROR:    "{BG:red}{FG:white+} {levelname} {R}    "
                      "{FG:red}{message}{R}",

            CRITICAL: "{BG:white+}{FG:red} {levelname} {R} "
                      "{FG:red}{message}{R}",
        }
        super().__init__(fmt, datefmt, style='%')

    def formatMessage(self, record):
        return self.format_by_level.get(
            record.levelno, self._fmt
        ).format(**record.__dict__)


def init_interactive_logging(level=logging.DEBUG):
    """
    Initialize the 'climactic' parent logger.

    In general, a library should not initialize/configure
    logging. This method is only to be called by the
    climactic command-line utility.

    :param level: a logging level from py:mod:`logging`
    """
    climactic_logger = logging.getLogger("climactic")
    climactic_logger.handlers.clear()

    handler = logging.StreamHandler()
    formatter = PerLevelFormatter()
    handler.setFormatter(formatter)
    climactic_logger.addHandler(handler)

    climactic_logger.setLevel(level)
    return climactic_logger


if __name__ == "__main__":
    init_interactive_logging(TRACE)

    logger = logging.getLogger("climactic.log")

    assert isinstance(logger, ExtendedLogger)

    logger.setLevel(TRACE)
    logger.trace("hey {FG:red}guy!")
    logger.debug("hey {FG:red}guy!")
    logger.info("hey {FG:red}guy!")
    logger.warn("hey {FG:red}guy!")
    logger.error("hey {FG:red}guy!")
    logger.critical("hey {FG:red}guy!")
