#! /usr/bin/env python
"""
"""
import os
import logging
import unittest
import yaml
from pathlib import Path
from yaml.scanner import ScannerError

from climactic.commands import CommandFactory
from climactic.errors import ClimacticUserError
from climactic.utility import cd_temp_dir


logger = logging.getLogger(__name__)


class CliTestCase(unittest.TestCase):

    """
    """

    @classmethod
    def from_path(cls, path, base_path=None):
        """
        Loads a test case from a YAML file.

        :param path (str, Path): The input file path
        :return (CliTestCase):
        """
        path = Path(path)
        with path.open() as f:
            try:
                task_list = yaml.load(f)
            except ScannerError as exc:
                raise ClimacticUserError(
                    (
                        "Invalid YAML syntax"
                        "\n{}\n{}\n{}"
                    ).format(
                        exc.context_mark,
                        exc.problem.replace(
                            "could not found",
                            "could not find"
                        ),
                        exc.problem_mark
                    )
                )
        return cls(
            task_list,
            path=path,
            base_path=base_path
        )

    def __init__(self, task_list, path=None, base_path=None):
        super().__init__()
        self.commands = []
        self.path = Path(path)
        if path and not base_path:
            raise ValueError(
                "base_path must be specified "
                "when path is specified"
            )
        self.base_path = Path(base_path)

        if not isinstance(task_list, list):
            raise RuntimeError(
                ("Parse error in {} "
                 "(YAML file does not evaluate "
                 "to a list)").format(
                    path
                )
            )

        for task_dict in task_list:
            if not isinstance(task_dict, dict):
                raise RuntimeError(
                    ("Parse error in {} "
                     "(YAML for task does not evaluate "
                     "to a dict)").format(
                        path or "<unknown>"
                    )
                )
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

    def __str__(self):
        if self.base_path:
            return str(self.path.relative_to(
                self.base_path
            ))
        return str(self.path)
