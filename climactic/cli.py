#! /usr/bin/env python
"""
"""
from climactic.runner import CliTestRunner

def main(root_dir):
    result = CliTestRunner.run_in_dir(root_dir)
    status = 0 if result.wasSuccessful() else 1
    return status
