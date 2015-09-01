#! /usr/bin/env python


class NameTag(object):

    """
    Sets the name of a test (useful for putting
    multiple tests in the same file)::

        ---
        - name: "My Test"

        ---
        - name: "My Second Test"
    """

    NAME = "name"

    def __init__(self, spec):
        assert isinstance(spec, str), "name requires one string argument"
        self.value = spec


tags = [
    NameTag
]
