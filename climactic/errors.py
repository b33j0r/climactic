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


class ClimacticSyntaxError(ClimacticUserError):

    """
    Something was wrong with user input
    in a test file (.yml).
    """


class ClimacticUnknownTagError(ClimacticSyntaxError):

    """
    Something was wrong with user input
    in a test file (.yml).
    """
