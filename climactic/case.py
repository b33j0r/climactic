#! /usr/bin/env python
"""
``climactic.case``
------------------

.. autoclass:: CliTestCase
"""
import logging
import unittest
from pathlib import Path

from climactic.command import Command
import climactic.assertion  # noqa
from climactic.errors import ClimacticBug, ClimacticSyntaxError
from climactic.tag import Tag
from climactic.parser import Parser
from climactic.utility import ClimacticTempDir


logger = logging.getLogger(__name__)


class CliTestCase(unittest.TestCase):

    """
    """

    @classmethod
    def from_path(cls, path, base_path=None):
        """
        Loads test cases from a YAML file.

        :param path: The input file path
        :type path: (str, Path)
        :rtype: generator
        """
        path = Path(path)
        parser = Parser()
        for task_list in parser.iparse_file(path):
            yield cls(
                task_list,
                path=path,
                base_path=base_path
            )

    def __init__(self, tags, path=None, base_path=None):
        super().__init__()
        self.commands = []
        self.path = Path(path)

        if base_path:
            self.base_path = Path(base_path)
        else:
            self.base_path = self.path.parent

        if not isinstance(tags, list):
            raise ClimacticSyntaxError(
                ("Parse error in {} "
                 "(YAML file does not evaluate "
                 "to a list)").format(
                    path
                )
            )

        for tag in tags:

            if isinstance(tag, Command):
                self.commands.append(tag)

            elif isinstance(tag, Tag):
                setattr(
                    self,
                    tag.NAME,
                    tag.value
                )

            else:
                raise ClimacticBug((
                    "Parser returned a {}; expected "
                    "Command or Tag:\n{}"
                ).format(
                    type(tag).__name__,
                    repr(tag)
                ))

    def runTest(self):
        with ClimacticTempDir():
            for command in self.commands:
                command.run(None, self)

    def __str__(self):
        name = getattr(self, "name", None)
        if name:
            return name
        if self.base_path:
            return str(
                self.path.relative_to(
                    self.base_path
                )
            )
        return str(self.path)
