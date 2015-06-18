#! /usr/bin/env python
"""
"""

import os

from climactic import command


def test_env_command():
    c = command.EnvCommand({
        "A": "a"
    })
    os.environ["A"] = "not-a"
    c.run(None, None)
    assert os.environ["A"] == "a"


def test_write_file_utf8(temp_dir):
    file_name = "hello"
    file_text = "hello!"
    file_path = (temp_dir / file_name)
    c = command.WriteFileUtf8Command({
        file_name: file_text
    })
    assert not file_path.exists()
    c.run(None, None)
    assert file_path.exists()
    actual_file_text = file_path.open().read()
    assert file_text == actual_file_text
