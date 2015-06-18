#! /usr/bin/env python
"""
"""

import pytest
from climactic.utility import ClimacticTempDir


@pytest.fixture(scope="function")
def temp_dir(request):
    d = ClimacticTempDir()
    temp_dir_path = d.__enter__()

    def cleanup_temp_dir():
        d.__exit__(None, None, None)

    request.addfinalizer(cleanup_temp_dir)

    return temp_dir_path
