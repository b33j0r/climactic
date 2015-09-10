#! /usr/bin/env python
"""
``climactic.errors``
--------------------

.. autoclass:: ClimacticError

.. autoclass:: ClimacticUserError

.. autoclass:: ClimacticSyntaxError

.. autoclass:: ClimacticUnknownTagError

"""


class ClimacticError(Exception):

    """
    Base climactic exception.
    """


class ClimacticBug(ClimacticError):

    """
    A meta-assertion about climactic's
    behavior. i.e. something that shouldn't
    happen, but did--whoops!
    """


class ClimacticUserError(ClimacticError):

    """
    Something is invalid in user input.
    """


class ClimacticSyntaxError(ClimacticUserError):

    """
    Something was wrong with user input
    in a test file (.yml).
    """


class ClimacticUnknownTagError(ClimacticSyntaxError):

    """
    A tag in a test file was misspelled
    or is not defined.
    """
