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
    "-v", "--verbose",
    action='store_const',
    const=2,
    dest='verbosity'
)


parser.add_argument(
    "-vv", "--debug",
    action='store_const',
    const=3,
    dest='verbosity'
)


def main(*args):
    global logger
    args = args or sys.argv[1:]

    try:
        namespace = parser.parse_args(args)

        # Specifying -v without an argument assumes 2.
        # Note that "default" above in the parser
        # is 1, which applies only if -v is not
        # specified at all

        # If -v is specified without an argument, it is
        # None

        verbosity = namespace.verbosity

        if verbosity in [1]:
            level = logging.WARN
        elif verbosity in [2, None]:
            level = logging.INFO
        elif verbosity in [3]:
            level = logging.DEBUG
        else:
            raise ClimacticUserError((
                "Verbosity level {} is invalid. "
                "Choose from 1, 2 or 3."
            ).format(verbosity))

        init_interactive_logging(level)
        logger = logging.getLogger(__name__)

        logger.debug("Initialized logger")

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
