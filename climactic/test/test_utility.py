#! /usr/bin/env python
"""
"""
from climactic.utility import substitute_env_vars


def test_substitute_env_vars_dict():
    template = "a string containing ${A_VAR}"
    expected = "a string containing foo"
    actual = substitute_env_vars(template, dict(A_VAR="foo"))
    assert expected == actual
