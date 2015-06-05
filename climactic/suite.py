#! /usr/bin/env python
"""
"""
import logging
import unittest
from pathlib import Path
import yaml
from climactic.commands import CommandFactory
from climactic.utility import cd_temp_dir


logger = logging.getLogger(__name__)


class CliTestCaseState:

    """
    """

    def __init__(self):
        self.env = {}


class CliTestSuite(unittest.TestSuite):

    """
    """

    @classmethod
    def from_dir(cls, dir_path, recursive=True):
        raise NotImplementedError()


class CliTestCase(unittest.TestCase):

    """
    """

    def __init__(self, task_list):
        super().__init__()
        self.commands = []

        for task_dict in task_list:
            commands = CommandFactory.build_commands(task_dict)
            self.commands.extend(commands)

    @classmethod
    def from_path(cls, path):
        """
        Loads a test case from a YAML file.

        :param path (str, Path): The input file path
        :return (CliTestCase):
        """
        path = Path(path)
        with path.open() as f:
            task_list = yaml.load(f)
        return cls(task_list)

    def runTest(self):
        with cd_temp_dir():
            logger.debug("setup")
            for command in self.commands:
                command.setup(None)

            logger.debug("run")
            for command in self.commands:
                command.run(None, self)

            logger.debug("teardown")
            for command in self.commands:
                command.teardown(None)
