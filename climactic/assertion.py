#! /usr/bin/env python
"""
``climactic.assertion``
-----------------------

Assertions are commands used to test a condition,
such as the existence of a file, the output of
the last command, etc. Assertions are executed in
the order they appear in the test file YAML
(because an Assertion is implemented as a
Command).

.. autoclass:: Assertion

.. autoclass:: AssertOutputCommand

.. autoclass:: AssertTreeCommand

.. autoclass:: AssertFileUtf8Command
"""
import os
import logging
from pathlib import Path

from climactic.command import Command
from climactic.utility import substitute_env_vars


logger = logging.getLogger(__name__)


class Assertion(Command):

    """
    Base class for assertions.
    """

    is_abstract = True


class AssertOutputCommand(Assertion):

    """
    Test condition command. Asserts that the
    output of the last command matches a given
    string::

        ---
        # A very simple test!

        - !run >
            echo Hello world!

        - !assert-output >
            Hello world!
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


class AssertTreeCommand(Assertion):

    """
    Test condition command. Asserts that the
    specified directory tree exists. Children which
    are dicts are validated as directories, and
    children which are strings are validated as files::

        - run: |
            mkdir hello
            touch hello/world.txt

        - assert-tree:
            hello:
            - world.txt
    """

    NAME = "assert-tree"

    def __init__(self, spec):
        self.paths = self._parse_paths(spec)

    def run(self, state, case):
        for path, type_str in self.paths:
            logger.debug(
                "assert-tree   {:4}    {}",
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


class AssertFileUtf8Command(Assertion):

    """
    Test condition command. Asserts that the
    contents of the specified file match the
    given utf-8 plaintext::

        - write-file-utf8:
            hello.txt: Hello world!

        - assert-file-utf8:
            hello.txt: Hello world!
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
