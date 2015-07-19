#! /usr/bin/env python
"""
``climactic.runner``
--------------------


"""
import unittest
import logging

from climactic.suite import CliTestSuite


logger = logging.getLogger(__name__)


class CliTestResult(unittest.TextTestResult):

    """
    """

    def __init__(self, stream, descriptions, verbosity):
        super().__init__(stream, descriptions, verbosity)

    def startTest(self, test):
        super(CliTestResult, self).startTest(test)
        if logger.parent.level < logging.INFO:
            # the superclass writes "
            self.stream.write("\n")
            self.stream.flush()


class CliTestRunner(unittest.TextTestRunner):

    """
    """

    resultclass = CliTestResult

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def run_for_targets(cls, *targets, recursive=True, **kwargs):
        runner = cls(**kwargs)
        suite = CliTestSuite.from_targets(
            *targets, recursive=recursive
        )
        result = runner.run(suite)
        return result

    @classmethod
    def run_in_dir(cls, dir_path, recursive=True, **kwargs):
        runner = cls(**kwargs)
        suite = CliTestSuite.from_dir(
            dir_path, recursive=recursive
        )
        result = runner.run(suite)
        return result
