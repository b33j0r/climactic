#! /usr/bin/env python
"""
Contains tests for `climactic.utility`
"""
import os
import pathlib
import tempfile
import pytest

from climactic.utility import (
    substitute_env_vars,
    ClimacticTempDir
)


def test_temp_dir_returns_pathlib_path():
    with ClimacticTempDir() as d:
        assert isinstance(d, pathlib.Path)


def test_temp_dir_returns_pathlib_path_under_tempdir():
    temp_root = pathlib.Path(tempfile.gettempdir()).resolve()
    with ClimacticTempDir() as d:
        assert d.relative_to(temp_root)


def test_temp_dir_returns_pathlib_path_not_under_old_cwd():
    original_cwd = pathlib.Path(os.getcwd())
    with ClimacticTempDir() as d:
        with pytest.raises(ValueError):
            d.relative_to(original_cwd)


def test_temp_dir_changes_directory():
    original_cwd = pathlib.Path(os.getcwd())
    with ClimacticTempDir():
        cwd = pathlib.Path(os.getcwd())
        assert cwd != original_cwd


def test_temp_dir_changes_directory_to_given_value():
    with ClimacticTempDir() as d:
        cwd = pathlib.Path(os.getcwd())
        assert cwd == d


def test_temp_dir_changes_directory_back():
    original_cwd = pathlib.Path(os.getcwd())
    with ClimacticTempDir():
        pass
    cwd = pathlib.Path(os.getcwd())
    assert cwd == original_cwd


def test_temp_dir_changes_directory_back_even_after_error():
    original_cwd = pathlib.Path(os.getcwd())
    with pytest.raises(Exception), ClimacticTempDir():
        raise Exception("whoops")
    cwd = pathlib.Path(os.getcwd())
    assert cwd == original_cwd


fixture_temp_dir = None


def test_temp_dir_pytest_fixture(request, temp_dir):
    assert isinstance(temp_dir, pathlib.Path)
    assert temp_dir.exists()
    temp_root = pathlib.Path(tempfile.gettempdir()).resolve()
    assert temp_dir.relative_to(temp_root)

    global fixture_temp_dir
    fixture_temp_dir = temp_dir


def teardown_module(module):
    """
    To fully test the temp_dir fixture, we need to check
    that fixture_temp_dir was populated and that the dir
    it specifies no longer exists.
    """
    assert fixture_temp_dir is not None
    assert isinstance(fixture_temp_dir, pathlib.Path)
    assert not fixture_temp_dir.exists()


def test_substitute_env_vars_dict():
    template = "a string containing ${A_VAR}"
    expected = "a string containing foo"
    actual = substitute_env_vars(template, dict(A_VAR="foo"))
    assert expected == actual
