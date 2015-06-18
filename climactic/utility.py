#! /usr/bin/env python
"""
"""
import os
import pathlib
import string
import tempfile
import logging


logger = logging.getLogger(__name__)


class ClimacticTempDir(tempfile.TemporaryDirectory):

    """
    Changes the current working directory to a temporary
    directory and deletes it after the context manager
    exits. Also sets the restores the CWD environment
    variable.

    NOTE: also yields a pathlib.Path object instead of
          a string
    """

    def __enter__(self):
        self.original_cwd = os.getcwd()
        self.original_cwd_var = os.environ.get("CWD")
        val = super().__enter__()
        os.chdir(val)
        os.environ["CWD"] = os.getcwd()
        return pathlib.Path(val).resolve()

    def __exit__(self, exc, value, tb):
        os.chdir(self.original_cwd)
        if self.original_cwd_var is None:
            del os.environ["CWD"]
        else:
            os.environ["CWD"] = self.original_cwd_var
        super().__exit__(exc, value, tb)


def substitute_env_vars(s, environ=None):
    """
    Performs bash-style string substitution on substrings
    matching the form ${VAR_NAME}

    :param s: string to make substitutions within
    :return: the resulting string
    """
    environ = environ or os.environ
    return string.Template(s).safe_substitute(environ)
