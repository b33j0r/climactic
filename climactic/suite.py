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
    def from_targets(cls, *targets, **kwargs):
        suite = cls()
        tests = []
        for target in targets:
            target_path = Path(target).resolve()

            if target_path.is_dir():
                target_tests = cls.collect_dir(
                    target_path,
                    **kwargs
                )
                tests.extend(target_tests)

            else:
                for target_test in cls.collect_file(
                    target_path
                ):
                    tests.append(target_test)
        suite.addTests(tests)
        return suite

    @classmethod
    def from_dir(cls, dir_path, **kwargs):
        return cls.from_targets(dir_path, **kwargs)

    @classmethod
    def collect_dir(cls, dir_path, recursive=True):
        tests = []

        dir_path = Path(dir_path)
        target_paths = dir_path.glob(
            ("**" if recursive else "*") +
            "/test_*.yml"
        )

        for target_path in target_paths:
            for test in cls.collect_file(
                target_path,
                base_path=dir_path
            ):
                tests.append(test)
        return tests

    @classmethod
    def collect_file(cls, target_path, base_path=None):
        logger.debug(
            "Loading yml file %r",
            target_path
        )
        yield from CliTestCase.from_path(
            target_path,
            base_path=base_path
        )
