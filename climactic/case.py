#! /usr/bin/env python
"""
``climactic.case``
------------------

.. autoclass:: ClimacticTestCase
"""
import logging
import unittest
from pathlib import Path

from climactic.errors import ClimacticSyntaxError
from climactic.parser import ClimacticParser
from climactic.utility import ClimacticTempDir


from climactic.plugins.discovery import load_plugins
load_plugins()


logger = logging.getLogger(__name__)


class ClimacticTestCase(unittest.TestCase):

    @classmethod
    def from_path(cls, path, base_path=None):
        """
        Loads test cases from a YAML file.

        :param path: The input file path
        :type path: (str, Path)
        :rtype: generator
        """
        path = Path(path)
        parser = ClimacticParser()
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

            try:
                setattr(
                    self,
                    tag.NAME,
                    tag.value
                )
            except AttributeError:
                self.commands.append(tag)

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
