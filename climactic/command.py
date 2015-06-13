#! /usr/bin/env python
"""
Defines the commands that can be used at the
top-level of an input test YAML file.
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

        :param state (CliTestCaseState):
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


class AssertOutputCommand(Command):

    """
    Test condition command. Asserts that the
    output of the last command matches a given
    string
    """

    NAME = "assert-output"

    def __init__(self, spec):
        assert isinstance(spec, str)
        self.template = spec

    def run(self, state, case):
        expected = substitute_env_vars(self.template)
        try:
            actual = os.environ["OUTPUT"]
        except KeyError:
            case.fail("No command ran before assert-output")
        case.assertEqual(
            expected.strip(),
            actual.strip()
        )


class AssertTreeCommand(Command):

    """
    Test condition command. Asserts that the
    specified directory tree exists. Children which
    are dicts are validated as directories, and
    children which are strings are validated as files.
    """

    NAME = "assert-tree"

    def __init__(self, spec):
        self.paths = self._parse_paths(spec)

    def run(self, state, case):
        for path, type_str in self.paths:
            logger.debug(
                "assert-tree   %4s    %s",
                type_str.upper(), str(path)
            )
            case.assertTrue(
                path.exists(),
                msg="Path does not exist: {}".format(path)
            )
            if type_str == "dir":
                case.assertTrue(
                    path.is_dir(),
                    msg="Path exists, but "
                        "is not a directory: {}".format(path)
                )
            else:
                case.assertTrue(
                    path.is_file(),
                    msg="Path exists, but "
                        "is not a file: {}".format(path)
                )

    def _parse_paths(self, spec, root=None):
        if spec is None:
            return []
        if root is None:
            root = Path()
        if isinstance(spec, str):
            return [
                (root/spec, "file")
            ]
        if isinstance(spec, list):
            return self._parse_paths_list(root, spec)
        if isinstance(spec, dict):
            return self._parse_paths_dict(root, spec)
        raise NotImplementedError("spec: {}".format(spec))

    def _parse_paths_list(self, root, spec):
        paths = []
        for child in spec:
            subpaths = self._parse_paths(child, root=root)
            paths.extend(subpaths)
        return paths

    def _parse_paths_dict(self, root, spec):
        paths = []
        for subdir, child_spec in spec.items():
            subdir_path = root / subdir
            paths.append((subdir_path, "dir"))
            subdir_paths = self._parse_paths(
                child_spec, root=subdir_path
            )
            if subdir_paths:
                paths.extend(subdir_paths)
        return paths


class AssertFileUtf8Command(Command):

    """
    Test condition command. Asserts that the
    contents of the specified file match the
    given utf-8 plaintext.
    """

    NAME = "assert-file-utf8"

    def __init__(self, spec):
        self.data = {
            file_path: contents for file_path, contents
            in spec.items()
        }

    def run(self, state, case):
        for file_path, expected in self.data.items():
            file_path = Path(file_path)
            case.assertTrue(file_path.exists())
            with file_path.open() as f:
                actual = f.read()
            case.assertEqual(
                expected.strip(),
                actual.strip()
            )


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
