#! /usr/bin/env python
"""
"""
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
from climactic.errors import ClimacticError
from climactic.runner import CliTestRunner


logger = logging.getLogger(__name__)


parser = argparse.ArgumentParser(
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
    "-v", "--verbosity",
    nargs="?",
    type=int,
    default=1
)


def main(*args):
    args = args or sys.argv[1:]
    namespace = parser.parse_args(args)
    try:
        result = CliTestRunner.run_in_dir(
            *namespace.target,
            verbosity=namespace.verbosity
        )
        status = 0 if result.wasSuccessful() else 1
        return status
    except ClimacticError as exc:
        logger.error(exc)
        return 2


if __name__ == "__main__":
    main(*(sys.argv[:1]))
