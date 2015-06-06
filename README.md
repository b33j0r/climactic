# ``climactic``

*Testing commandline utilities*

A simple testing framework for running
shell commands and verifying their behavior. Tests are
written as YAML files which specify the commands to run
along with assertions about the output (currently, stdout
and file/directory contents).

**NOTE: ``climactic`` is a Python 3.4+ package**

### Features
- Aggregate tests recursively in a directory matching the
  pattern ``test_*.yml`` using the commandline tool
  ``climactic``
- Compatibility with the standard ``unittest`` package
- Tests are run in a temporary directory to avoid data loss
  and path-dependent results
- Set environment variables per-test with the ``env`` task
- Compare stdout, directory structure, and file contents
  to expected string values
- ``bash``-like ``${VAR}`` substitution for input commands
  and output validation


## Install

To use the most recent source code (recommended at this time,
as development is very active):

virtualenv -p python3 climactic_venv
source climactic_venv/bin/activate
pip install -U -e git+https://github.com/b33j0r/climactic.git#egg=climactic

``climactic`` is registered in PyPI, so pip works too:

    pip install climactic

Either method will install the ``climactic`` python package
as well as the ``climactic`` commandline utility.


## Usage Example

Create a test file ``test_git_init.yml``:

    ---
    # Run `git init` and verify that
    # the expected directory structure
    # and file contents are produced.
    
    # Sets environment vars
    - env:
        CMD: git
    
    # Runs `git init`
    - run: |
        ${CMD} init
    
    # Verifies the dir tree and files
    # were created
    - assert-tree:
      - .git:
        - HEAD
        - objects:
        - refs:
          - heads:
          - tags:
    
    # Verifies that the file .git/HEAD
    # was populated with the ref string
    # for the initial master branch
    - assert-file-utf8:
      - .git/HEAD: |
          refs/heads/master

``cd`` to a directory containing this file and run:

    ~/climactic/examples$ climactic
    .
    ----------------------------------------------------------------------
    Ran 1 test in 0.029s
    
    OK


## License

Copyright (C) 2015  Brian Jorgensen

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.


## Author

[Brian Jorgensen](brian.jorgensen+climactic@gmail.com)

*Don't Take Any Wooden Nickels*
