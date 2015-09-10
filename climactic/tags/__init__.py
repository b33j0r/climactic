#! /usr/bin/env python
"""
Metadata
--------

.. automodule:: climactic.tags.metadata


Assertions
----------

.. automodule:: climactic.tags.assertions


Filesystem
----------

.. automodule:: climactic.tags.filesystem


Process Control
---------------

.. automodule:: climactic.tags.processes

"""

from itertools import chain

from climactic.tags import (
    metadata,
    assertions,
    processes
)
from climactic.tags import filesystem

tags = chain(
    assertions.tags,
    processes.tags,
    metadata.tags,
    filesystem.tags,
)
