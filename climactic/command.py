#! /usr/bin/env python
"""
``climactic.command``
---------------------


Defines the commands that can be used at the
top-level of an input test YAML file. Commands
are executed in order and "do something".
"""
import os
import subprocess
import logging
from pathlib import Path
from abc import abstractmethod

from climactic.tag import Tag
from climactic.utility import substitute_env_vars


logger = logging.getLogger(__name__)


ENV = os.environ.copy()


class Command(Tag):

    """
    Base class for all commands that can be used in
    test YAML files
    """

    is_abstract = True

    @abstractmethod
    def run(self, state, case):
        """
        Does the thing the subclass says it will do!

        :param state:
        :type state CliTestCaseState:
        :param case (unittest.TestCase):
        """


class EnvCommand(Command):

    """
    Exports environment variables.
    """
    NAME = "env"

    def __init__(self, spec):
        self.env = {}
        for key, value in spec.items():
            self.env[key] = value

    def run(self, state, case):
        os.environ.update(self.env)


class RunCommand(Command):

    """
    Runs one or more lines of bash-style commands.
    ${VAR} replacement is performed on each command
    using the current environment variables.
    """

    NAME = "run"

    def __init__(self, spec):
        try:
            self.cmd_lines = spec.split('\n')
        except AttributeError:
            self.cmd_lines = list(spec)

        self.cmd_lines = [
            cmd_line for cmd_line in self.cmd_lines
            if cmd_line.strip()
        ]

    def run(self, state, case):
        outputs = []
        for cmd_line in self.cmd_lines:
            cmd_args = [
                substitute_env_vars(arg)
                for arg in cmd_line.split(" ")
            ]
            logger.info("Running `%s`", " ".join(cmd_args))
            output_bytes = subprocess.check_output(cmd_args)
            output = output_bytes.decode()
            logger.info("Output:\n---\n%s---", output)
            outputs.append(output)
        os.environ["OUTPUT"] = "\n".join(outputs)


class WriteFileUtf8Command(Command):

    """
    Writes text to a file, encoded in utf-8.
    """

    NAME = "write-file-utf8"

    def __init__(self, spec):
        assert len(spec) == 1
        self.path, self.contents = next(
            iter(
                spec.items()
            )
        )
        self.path = Path(self.path)

    def run(self, state, case):
        with (Path(os.getcwd())/self.path).open('w') as f:
            f.write(self.contents)
        os.environ["OUTPUT"] = ""
