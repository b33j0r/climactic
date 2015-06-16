#! /usr/bin/env python
"""
climactic
YAML-based tests for commandline utilities


Copyright (C) 2015  Brian Jorgensen

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the

Free Software Foundation, Inc.
51 Franklin Street, Fifth Floor
Boston, MA
02110-1301, USA.
"""

import logging


logging.basicConfig(level=logging.WARN)

PROJECT_AUTHOR = "Brian Jorgensen <brian.jorgensen@gmail.com>"

PROJECT_COPYRIGHT_YEAR = "2015"

PROJECT_VERSION = '0.3.0'

PROJECT_URL = 'https://github.com/b33j0r/climactic'

PROJECT_DESCRIPTION = """
YAML-based tests for commandline utilities
""".strip()

PROJECT_LONG_DESCRIPTION_NO_FEATURES = """
A simple testing framework for running shell commands and \
verifying their behavior. Tests are written as YAML files \
which specify the commands to run, along with assertions \
about the output (currently, stdout and file/directory \
contents).
""".strip()

PROJECT_LONG_DESCRIPTION = (
    PROJECT_LONG_DESCRIPTION_NO_FEATURES +
    """

NOTE: climactic is a Python 3 package

Features

* Pytest integration via an automatically registered plugin
* Aggregate tests recursively in a directory matching the \
pattern "test_*.yml" using the commandline tool `climactic`
* Compatibility with the standard `unittest` package
* Tests are run in a temporary directory to avoid data loss \
and path-dependent results
* Set environment variables per-test with the 'env' task
* Compare stdout, directory structure, and file contents to \
expected string values
* bash-like ${VAR} substitution for input commands and output \
validation
"""
).strip()
