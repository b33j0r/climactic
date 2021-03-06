#! /usr/bin/env python
"""
``climactic.cli``
-----------------

The command-line interface to climactic's test runner,
which is based on :py:mod:`unittest`.
"""

import os
from pprint import pformat
import sys
import argparse
import textwrap
import logging

from climactic.log import init_interactive_logging


init_interactive_logging(logging.CRITICAL)
logger = logging.getLogger(__name__)


from climactic import (
    PROJECT_LONG_DESCRIPTION_NO_FEATURES,
    PROJECT_VERSION,
    PROJECT_COPYRIGHT_YEAR,
    PROJECT_AUTHOR
)


from climactic.errors import ClimacticError, ClimacticUserError
from climactic.log import TRACE


class ArgumentParserError(Exception):
    """
    """


class ClimacticArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        raise ClimacticUserError(message)


parser = ClimacticArgumentParser(
    description=textwrap.fill(
        PROJECT_LONG_DESCRIPTION_NO_FEATURES
    ),
    epilog="""
ABOUT
-----
climactic v{PROJECT_VERSION}
Copyright (C) \
{PROJECT_COPYRIGHT_YEAR} \
{PROJECT_AUTHOR}

WEBSITE
-------
https://github.com/b33j0r/climactic

LICENSING
---------
Climactic comes with ABSOLUTELY NO WARRANTY; for details see:
https://github.com/b33j0r/climactic/blob/master/LICENSE
.
""".format(
        PROJECT_VERSION=PROJECT_VERSION,
        PROJECT_COPYRIGHT_YEAR=PROJECT_COPYRIGHT_YEAR,
        PROJECT_AUTHOR=PROJECT_AUTHOR
    ),
    formatter_class=argparse.RawTextHelpFormatter
)


parser.add_argument(
    "target",
    nargs="*",
    help="Files and/or directories to test",
    default=["."]
)


parser.add_argument(
    "--logging-test",
    action="store_true",
    help="Log a string at each logging level",
    dest="logging_test"
)


parser.add_argument(
    "--verbosity",
    type=int,
    default=os.environ.get("CLIMACTIC_LOG_LEVEL", 1),
    dest='verbosity',
    help="Directly sets verbosity to 0-3 "
         "(quiet, normal, verbose, or debug)"
)


parser.add_argument(
    "-q", "--quiet",
    action='store_const',
    const=0,
    dest='verbosity',
    help="Log as little as possible, only serious problems (CRITICAL)"
)


parser.add_argument(
    "-v", "--verbose",
    action='store_const',
    const=2,
    dest='verbosity',
    help="Log additional information, but not _everything_ (INFO)"
)


parser.add_argument(
    "-vv", "--debug",
    action='store_const',
    const=3,
    dest='verbosity',
    help="Log almost everything (DEBUG)"
)


parser.add_argument(
    "-vvv", "--trace",
    action='store_const',
    const=4,
    dest='verbosity',
    help="Log everything available (TRACE)"
)


def _decide_verbosity_and_log_level(verbosity):
    """
    """
    verbosity_level = {
        0: logging.CRITICAL,
        1: logging.WARN,
        2: logging.INFO,
        3: logging.DEBUG,
        4: TRACE
    }
    try:
        level = verbosity_level[verbosity]
    except KeyError:
        raise ClimacticUserError((
            "Verbosity level {} is invalid. "
            "Choose from 0, 1, 2, 3, or 4."
        ).format(verbosity))

    return level, verbosity


def main(*args):
    global logger
    args = args or sys.argv[1:]

    try:
        namespace = parser.parse_args(args)

        logging_level, verbosity = (
            _decide_verbosity_and_log_level(namespace.verbosity)
        )

        logger = init_interactive_logging(logging_level)

        if namespace.logging_test:
            logger.info(
                "{R}Previewing terminal colors and log level outputs: "
                "{fg:r}r{fg:y}y{fg:g}g{fg:b}b{fg:i}i{fg:v}v{fg:w}w"
                "{bg:w}{fg:d}d{fg:$}"
            )
            logger.trace("a TRACE message")
            logger.debug("a DEBUG message")
            logger.info("an INFO message")
            logger.warning("a WARNING message")
            logger.error("an ERROR message")
            logger.critical("a CRITICAL message")

        # This is currently when tag loading happens,
        # so we want to do it after logging is set up
        # so that the registration of tags can be logged
        # at the TRACE level
        from climactic.runner import ClimacticTestRunner

        logger.trace(
            "climactic cli invoked with: {}",
            pformat(vars(namespace))
        )
        result = ClimacticTestRunner.run_for_targets(
            *namespace.target,
            verbosity=verbosity
        )
        return 0 if result.wasSuccessful() else 1

    except ClimacticError as exc:
        logger.error(exc)
        return 2

    except Exception as exc:
        logger.exception("Unhandled exception")
        logger.critical(exc)
        return 3


def json_env(*args):
    import os
    import json

    print(
        json.dumps(
            {
                k: str(v)
                for k, v in os.environ.items()
            },
            indent=2
        )
    )


if __name__ == "__main__":
    main()
