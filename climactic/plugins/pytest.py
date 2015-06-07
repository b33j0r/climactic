#! /usr/bin/env python
"""
"""

import pytest
from pathlib import Path

from climactic.case import CliTestCase


def pytest_collect_file(parent, path):
    if path.ext == ".yml" and path.basename.startswith("test"):
        return YamlFile(path, parent)

class YamlFile(pytest.File):
    def collect(self):
        path = Path(str(self.fspath))
        self.climactic_case = CliTestCase.from_path(
            path,
            Path(str(self.parent.fspath))
        )
        yield from [
            YamlItem(
                path.parts[-1],
                self.parent,
                self.climactic_case
            )
        ]

class YamlItem(pytest.Item):
    def __init__(self, name, parent, climactic_case):
        super(YamlItem, self).__init__(name, parent)
        self.ccase = climactic_case

    def runtest(self):
        self.ccase.runTest()
