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
        for climactic_case in CliTestCase.from_path(
            path,
            Path(str(self.parent.fspath))
        ):
            yield ClimacticPytestItem(
                self.fspath.basename,
                self,
                climactic_case
            )


class ClimacticPytestItem(pytest.Item):
    def __init__(self, name, parent, climactic_case):
        self.ccase = climactic_case
        super(ClimacticPytestItem, self).__init__(
            str(self.ccase), parent
        )

    def reportinfo(self):
        return self.fspath, None, str(self.ccase)

    def runtest(self):
        self.ccase.runTest()
