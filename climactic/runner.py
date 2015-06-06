#! /usr/bin/env python
"""
"""
import unittest

from climactic.suite import CliTestSuite


class CliTestRunner(unittest.TextTestRunner):

    """
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def run_in_dir(cls, dir_path, recursive=True, **kwargs):
        runner = cls(**kwargs)
        suite = CliTestSuite.from_dir(
            dir_path,
            recursive=recursive
        )
        result = runner.run(suite)
        return result

if __name__ == "__main__":
    CliTestRunner.run_in_dir(
        "/Users/brjorgensen/PycharmProjects/climactic/examples",
        verbosity=3
    )
