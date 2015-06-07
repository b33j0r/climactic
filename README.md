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
    # Run `git init` and verify
    # that the expected directory
    # structure and file contents
    # are produced.
    
    # Sets environment variables
    - env:
        CMD: git
        CMD_NAME: Git
        REPO_DIR: .git/
    
    # Runs `git init` in a new
    # temporary directory
    - run: |
        ${CMD} init
    
    # Checks that stdout was as
    # expected
    - assert-output: >
        Initialized empty ${CMD_NAME}
        repository in ${CWD}/${REPO_DIR}
    
    # Verifies that expected files
    # and directories were created
    - assert-tree:
        .git:
        - HEAD
        - objects:
        - refs:
          - heads:
          - tags:
    
    # Verifies that the HEAD file
    # has the correct initial value
    - assert-file-utf8:
        .git/HEAD: |
          ref: refs/heads/master


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
