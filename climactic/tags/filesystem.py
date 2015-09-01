#! /usr/bin/env python
"""
"""
import os
from pathlib import Path


class WriteFileUtf8Command(object):

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


tags = [
    WriteFileUtf8Command
]
