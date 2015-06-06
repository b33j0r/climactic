#! /usr/bin/env python
"""
"""
import logging
import unittest
from pathlib import Path

from climactic.case import CliTestCase

logger = logging.getLogger(__name__)


class CliTestSuite(unittest.TestSuite):

    """
    """

    @classmethod
    def from_dir(cls, dir_path, recursive=True):
        dir_path = Path(dir_path)
        target_paths = dir_path.glob(
            ("**" if recursive else "*") +
            "/test_*.yml"
        )
        suite = cls()
        tests = []
        for target_path in target_paths:
            logger.debug(
                "Loading yml file %r",
                target_path
            )
            test = CliTestCase.from_path(target_path)
            tests.append(test)
        suite.addTests(tests)
        return suite
