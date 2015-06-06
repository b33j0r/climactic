#! /usr/bin/env python
"""
"""
import logging
import unittest
import yaml
from pathlib import Path

from climactic.commands import CommandFactory
from climactic.utility import cd_temp_dir


logger = logging.getLogger(__name__)


class CliTestCase(unittest.TestCase):

    """
    """

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

    def __init__(self, task_list):
        super().__init__()
        self.commands = []

        for task_dict in task_list:
            commands = CommandFactory.build_commands(task_dict)
            self.commands.extend(commands)

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
