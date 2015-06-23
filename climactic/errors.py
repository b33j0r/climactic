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
    A tag in a test file was misspelled
    or is not defined.
    """
