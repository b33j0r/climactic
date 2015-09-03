#! /usr/bin/env python
"""
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
