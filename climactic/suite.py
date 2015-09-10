#! /usr/bin/env python
"""
``climactic.suite``
-------------------

.. autoclass:: ClimacticTestSuite
"""
import logging
import unittest
from pathlib import Path

from climactic.case import ClimacticTestCase


logger = logging.getLogger(__name__)


class ClimacticTestSuite(unittest.TestSuite):

    """
    A collection of tests.
    """

    @classmethod
    def from_targets(cls, *targets, **kwargs):
        suite = cls()
        tests = []
        logger.trace("Processing target list {}", list(targets))
        for target in targets:
            logger.trace("Processing target '{}'", target)
            try:
                target_path = Path(target).resolve()
            except FileNotFoundError:
                logger.warn(
                    "Target '{}' could not be found", target
                )
                continue

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
        logger.trace("+ Collecting dir {}", str(dir_path))
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
        logger.trace("- Collecting dir {}", str(dir_path))
        return tests

    @classmethod
    def collect_file(cls, target_path, base_path=None):
        logger.trace(
            "  + Loading yml file {!r}",
            str(target_path)
        )
        yield from ClimacticTestCase.from_path(
            target_path,
            base_path=base_path
        )
