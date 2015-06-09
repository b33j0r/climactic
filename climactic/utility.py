#! /usr/bin/env python
"""
"""
import os
import string
import tempfile
import shutil
import logging
from contextlib import contextmanager


logger = logging.getLogger(__name__)


@contextmanager
def cd_temp_dir():
    """
    Changes the current working directory to a temporary
    directory and deletes it after the context manager
    exits.
    """
    original_cwd = os.getcwd()
    temp_dir_path = tempfile.mkdtemp()
    os.chdir(temp_dir_path)
    os.environ["CWD"] = os.getcwd()
    assert os.environ["CWD"] != original_cwd
    logger.debug("Created temp dir %r", temp_dir_path)
    try:
        yield temp_dir_path
    finally:
        os.chdir(original_cwd)
        os.environ["CWD"] = os.getcwd()
        shutil.rmtree(temp_dir_path)
        logger.debug("Deleted temp dir %r", temp_dir_path)


def substitute_env_vars(s, environ=None):
    """
    Performs bash-style string substitution on substrings
    matching the form ${VAR_NAME}

    :param s: string to make substitutions within
    :return: the resulting string
    """
    environ = environ or os.environ
    return string.Template(s).safe_substitute(environ)
