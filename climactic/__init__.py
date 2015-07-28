#! /usr/bin/env python
"""
.. automodule:: climactic.assertion

.. automodule:: climactic.command

.. automodule:: climactic.tag

.. automodule:: climactic.cli

.. automodule:: climactic.case

.. automodule:: climactic.errors

.. automodule:: climactic.parser

.. automodule:: climactic.runner

.. automodule:: climactic.state

.. automodule:: climactic.suite

.. automodule:: climactic.utility
"""

import climactic.log

PROJECT_AUTHOR = "Brian Jorgensen <brian.jorgensen@gmail.com>"

PROJECT_COPYRIGHT_YEAR = "2015"

PROJECT_VERSION = '0.3.1'

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
