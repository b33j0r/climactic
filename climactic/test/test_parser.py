#! /usr/bin/env python
"""
"""
from io import StringIO
from collections import Sequence

import pytest

from climactic.tags.metadata import NameTag
from climactic.tags.processes import ShellRunCommand, EnvCommand
from climactic.tags.assertions import AssertOutputCommand
from climactic.errors import (
    ClimacticSyntaxError,
    ClimacticUnknownTagError
)
from climactic.parser import ClimacticParser


def parse_str(yaml_str):
    stream = StringIO(yaml_str)
    parser = ClimacticParser()
    tests = parser.parse_stream(stream)
    assert isinstance(tests, Sequence)
    assert not isinstance(tests, (str, bytes))
    return tests


def test_parse_empty_file():
    """
    Parsing an empty file should return a value
    which evaluates to a boolean False
    """
    yaml_str = ""
    tests = parse_str(yaml_str)
    assert not tests


def test_parse_empty_test():
    """
    """
    yaml_str = "#!yaml\n---\n"
    tests = parse_str(yaml_str)
    assert not tests


def test_parse_empty_tests():
    """
    """
    yaml_str = "#!yaml\n---\n---\n"
    tests = parse_str(yaml_str)
    assert not tests


def test_parse_scanner_error():
    """
    """
    yaml_str = "#!yaml\n---\n- stuff\n-other-stuff\n---\n"
    with pytest.raises(ClimacticSyntaxError):
        parse_str(yaml_str)


def test_parse_constructor_error():
    """
    """
    yaml_str = "#!yaml\n---\n!other-stuff"
    with pytest.raises(ClimacticUnknownTagError):
        parse_str(yaml_str)


def test_parse_one_simple_test_with_dict_syntax():
    """
    """
    yaml_str = """
#!yaml
---
- name: Name
- run: >
    echo Hello world!

- assert-output: >
    Hello world!
""".lstrip()
    tests = parse_str(yaml_str)
    assert len(tests) == 1
    test = tests[0]
    assert len(test) == 3
    assert isinstance(test[0], NameTag)
    assert test[0].value == "Name"
    assert isinstance(test[1], ShellRunCommand)
    assert test[1].cmd_lines == ["echo Hello world!"]
    assert isinstance(test[2], AssertOutputCommand)
    assert test[2].template.strip() == "Hello world!"


def test_parse_one_simple_test_with_tag_syntax():
    """
    """
    yaml_str = """
#!yaml
---
- !run >
    echo Hello world!

- !assert-output >
    Hello world!
""".lstrip()
    tests = parse_str(yaml_str)
    assert len(tests) == 1
    test = tests[0]
    assert len(test) == 2
    assert isinstance(test[0], ShellRunCommand)
    assert isinstance(test[1], AssertOutputCommand)


def test_parse_one_simple_test_with_mixed_syntax():
    """
    """
    yaml_str = """
#!yaml
---
- run: >
    echo Hello world!

- !assert-output >
    Hello world!
""".lstrip()
    tests = parse_str(yaml_str)
    assert len(tests) == 1
    test = tests[0]
    assert len(test) == 2
    assert isinstance(test[0], ShellRunCommand)
    assert isinstance(test[1], AssertOutputCommand)


def test_parse_two_simple_tests_with_mixed_syntax():
    """
    """
    yaml_str = """
#!yaml
---
- run: >
    echo Hello world!

- assert-output: >
    Hello world!

- env:
    A: 1
    B: 2
---
- !run >
    echo Hello world!

- !assert-output >
    Hello world!

- !env
    A: 1
    B: 2
""".lstrip()
    tests = parse_str(yaml_str)
    assert len(tests) == 2
    for test in tests:
        assert len(test) == 3
        assert isinstance(test[0], ShellRunCommand)
        assert isinstance(test[1], AssertOutputCommand)
        assert isinstance(test[2], EnvCommand)
        assert test[2].env == {"A": 1, "B": 2}
