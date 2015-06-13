#! /usr/bin/env python
"""
"""
import pytest
from collections import Sequence
from io import StringIO
from climactic import command
from climactic.errors import ClimacticUserError
from climactic.parser import Parser


def parse_str(yaml_str):
    stream = StringIO(yaml_str)
    parser = Parser()
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
    with pytest.raises(ClimacticUserError):
        parse_str(yaml_str)


def test_parse_one_simple_test_with_dict_syntax():
    """
    """
    yaml_str = """
#!yaml
---
- run: >
    echo Hello world!

- assert-output: >
    Hello world!
""".lstrip()
    tests = parse_str(yaml_str)
    assert len(tests) == 1
    test = tests[0]
    assert len(test) == 2
    assert isinstance(test[0], command.RunCommand)
    assert isinstance(test[1], command.AssertOutputCommand)


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
    assert isinstance(test[0], command.RunCommand)
    assert isinstance(test[1], command.AssertOutputCommand)


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
    assert isinstance(test[0], command.RunCommand)
    assert isinstance(test[1], command.AssertOutputCommand)


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
        assert isinstance(test[0], command.RunCommand)
        assert isinstance(test[1], command.AssertOutputCommand)
        assert isinstance(test[2], command.EnvCommand)
        assert test[2].env == {"A": 1, "B": 2}
