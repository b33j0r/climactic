#! /usr/bin/env python
"""
"""
import sys
import logging
import unittest
import yaml

from climactic.suite import CliTestCase, CliTestSuite


logger = logging.getLogger(__name__)


def main():
    test = CliTestCase.from_path("test_init.yml")

    runner = unittest.TextTestRunner(stream=sys.stdout)
    suite = CliTestSuite()
    suite.addTest(test)

    result = runner.run(suite)
    return result


if __name__ == "__main__":
    main()
