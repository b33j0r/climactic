#! /usr/bin/env python
"""
"""

import pytest
from pathlib import Path

from climactic.case import CliTestCase


def pytest_addoption(parser):
    parser.addini(
        "climactic_files",
        help="The file pattern used "
             "to collect climactic test files",
        default="test_*.yml"
    )


def pytest_configure(config):
    pattern = config.getini("climactic_files")
    plugin = ClimacticPytestPlugin(pattern)
    config.pluginmanager.register(plugin)


class ClimacticPytestPlugin:
    def __init__(self, pattern):
        self.pattern = pattern

    def pytest_collect_file(self, parent, path):
        if path.fnmatch(self.pattern):
            return ClimacticPytestFile(path, parent)


class ClimacticPytestFile(pytest.File):
    def collect(self):
        path = Path(str(self.fspath))
        self.climactic_case = CliTestCase.from_path(
            path,
            Path(str(self.parent.fspath))
        )
        yield ClimacticPytestItem(
            path.parts[-1],
            self,
            self.climactic_case
        )


class ClimacticPytestItem(pytest.Item):
    def __init__(self, name, parent, climactic_case):
        super(ClimacticPytestItem, self).__init__(name, parent)
        self.ccase = climactic_case

    def runtest(self):
        self.ccase.runTest()
