#! /usr/bin/env python
"""
"""


class ClimacticError(Exception):

    """
    Base climactic exception, used for
    handling errors which are not (known)
    bugs.
    """


class ClimacticUserError(ClimacticError):

    """
    Something went wrong in user input.
    """


class ClimacticTestSyntaxError(ClimacticError):

    """
    Something was wrong with user input
    in a test file (.yml).
    """
