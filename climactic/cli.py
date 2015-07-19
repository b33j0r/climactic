#! /usr/bin/env python
"""
``climactic.cli``
-----------------

The command-line interface to climactic's test runner,
which is based on :py:mod:`unittest`.
"""
import os
import sys
import argparse
import textwrap
import logging

from climactic import (
    PROJECT_LONG_DESCRIPTION_NO_FEATURES,
    PROJECT_VERSION,
    PROJECT_COPYRIGHT_YEAR,
    PROJECT_AUTHOR
)
from climactic.errors import ClimacticError, ClimacticUserError
from climactic.log import init_interactive_logging
from climactic.runner import CliTestRunner


init_interactive_logging()
logger = logging.getLogger(__name__)


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


parser.set_defaults(
    verbosity=os.environ.get("CLIMACTIC_LOG_LEVEL", 1)
)


parser.add_argument(
    "--verbosity",
    type=int,
    default=1,
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
    if verbosity == 0:
        level = logging.CRITICAL
    elif verbosity == 1:
        level = logging.WARN
    elif verbosity in [2, None]:
        level = logging.INFO
        verbosity = 2
    elif verbosity == 3:
        level = logging.DEBUG
    elif verbosity == 4:
        level = logging.TRACE
    else:
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
            _decide_verbosity_and_log_level(
                namespace.verbosity
            )
        )

        init_interactive_logging(logging_level)
        logger = logging.getLogger(__name__)

        logger.trace("Initialized logger")

        logger.debug(namespace)
        result = CliTestRunner.run_for_targets(
            *namespace.target,
            verbosity=verbosity
        )
        status = 0 if result.wasSuccessful() else 1
        return status

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
    main(*(sys.argv[:1]))
