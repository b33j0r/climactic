#! /usr/bin/env python
"""
``climactic.command``
---------------------

Defines the commands that can be used at the
top-level of an input test YAML file. Commands
are executed in order and "do something".

.. autoclass:: Command

.. autoclass:: ShellRunCommand

.. autoclass:: SubprocessRunCommand

.. autoclass:: EnvCommand

.. autoclass:: WriteFileUtf8Command
"""
from collections import OrderedDict
import json
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
    Exports environment variables::

        ---
        # A very simple test!

        - !env
            MY_STRING: "Hey guys!"

        - !run >
            echo ${MY_STRING}

        - !assert-output >
            Hey guys!
    """
    NAME = "env"

    def __init__(self, spec):
        self.env = {}
        for key, value in spec.items():
            self.env[key] = value

    def run(self, state, case):
        os.environ.update(self.env)


class SubprocessRunCommand(Command):

    """
    Runs one or more lines of bash-style commands.
    ``${VAR}`` replacement is performed on each command
    using the current environment variables::

        ---
        # A very simple test!

        - !run-subprocess >
            echo Hello world!

        - !assert-output >
            Hello world!
    """

    NAME = "run-subprocess"

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
            logger.debug("Running `{}`", " ".join(cmd_args))
            output_bytes = subprocess.check_output(cmd_args)
            output = output_bytes.decode()
            logger.debug("Output:\n{}", output.rstrip())
            outputs.append(output)
        os.environ["OUTPUT"] = "\n".join(outputs)


def dict_diff(before, after):
    diff = OrderedDict()
    for bk, bv in before.items():
        if bk not in after or bv != after[bk]:
            diff[bk] = bv
    for ak, av in after.items():
        if ak not in before or av != before[ak]:
            diff[ak] = av
    return diff


class ShellRunCommand(Command):

    """
    Runs one or more lines of shell commands
    using bash (will be extended in the future
    to use any shell)::

        ---
        # A very simple test!

        - !run >
            echo Hello world!

        - !assert-output >
            Hello world!
    """

    NAME = "run"
    ENV_SEPARATOR = "***climactic*end-of-stdout***"

    def __init__(self, spec):
        try:
            self.cmd_lines = spec.split('\n')
        except AttributeError:
            self.cmd_lines = list(spec)

        self.cmd_lines = [
            cmd_line for cmd_line in self.cmd_lines
            if cmd_line.strip()
        ]

        self.cmd_lines_suffix = [
            "echo " + self.ENV_SEPARATOR,
            "unset OUTPUT",
            "json-env"
        ]

        self.script_wo_suffix = "\n".join(self.cmd_lines)
        self.script = "\n".join(self.cmd_lines + self.cmd_lines_suffix)

    def run(self, state, case):
        original_env = os.environ.copy()
        cmd_args = [
            "/usr/bin/env", "bash"
        ]
        p = subprocess.Popen(
            cmd_args,
            stdout=subprocess.PIPE,
            stdin=subprocess.PIPE
        )
        logger.debug(
            "Running script with `{}`:\n{fg:w}{}{R}",
            " ".join(cmd_args),
            self.script_wo_suffix
        )
        script_bytes = self.script.encode()
        stdout, stderr = p.communicate(script_bytes)
        stdout, env = stdout.decode().split(self.ENV_SEPARATOR)
        stderr = stderr.decode() if stderr else ""
        if env.strip():
            env = json.loads(env)
        else:
            env = {}
        if stdout.strip():
            logger.debug("stdout:\n{fg:w}{}{R}", stdout.rstrip())
        if stderr.strip():
            logger.debug("stderr:\n{fg:w}{}{R}", stderr.rstrip())
        env_diff = dict_diff(original_env, env)
        logger.trace(
            "env changes:\n{fg:w}{}{R}",
            json.dumps(env_diff, indent=4)
        )

        os.environ["OUTPUT"] = stdout


class WriteFileUtf8Command(Command):

    """
    Writes text to a file, encoded in utf-8::

        ---
        # A simple test which writes to a file

        - write-file-utf8:
            hello.txt: Hello world!

        - assert-output: ""

        - assert-file-utf8:
            hello.txt: Hello world!
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
