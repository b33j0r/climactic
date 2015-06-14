#! /usr/bin/env python
"""
"""
import logging
import unittest
from pathlib import Path

from climactic.command import Command
from climactic.tag import TagFactory, Tag
from climactic.parser import Parser
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

        if path and not base_path:
            raise ValueError(
                "base_path must be specified "
                "when path is specified"
            )

        self.base_path = Path(base_path)

        if not isinstance(tags, list):
            raise RuntimeError(
                ("Parse error in {} "
                 "(YAML file does not evaluate "
                 "to a list)").format(
                    path
                )
            )

        for tag_or_dict in tags:

            if isinstance(tag_or_dict, Command):
                self.commands.append(tag_or_dict)
                continue

            if isinstance(tag_or_dict, Tag):
                setattr(
                    self,
                    tag_or_dict.NAME,
                    tag_or_dict.value
                )
                continue

            if not isinstance(tag_or_dict, dict):
                raise RuntimeError(
                    ("Parse error in {} "
                     "(YAML for task does not evaluate "
                     "to a dict)").format(
                        path or "<unknown>"
                    )
                )

            commands = TagFactory.build_tags(tag_or_dict)
            self.commands.extend(commands)

    def runTest(self):
        with cd_temp_dir():
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
