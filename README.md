# ``climactic``

*Testing commandline utilities*

A simple testing framework for running
shell commands and verifying their behavior. Tests are
written as YAML files which specify the commands to run
along with assertions about the output (currently, stdout
and file/directory contents).

**NOTE: ``climactic`` is a Python 3.4+ package**


### Hello, World!

``test_hello.yml``:

    ---
    # A very simple test!
    
    - run: >
        echo Hello world!
    
    - assert-output: >
        Hello world!

Run the test runner:

    ~$ climactic test_hello.yml
    .
    ----------------------------------------------------------------------
    Ran 1 test in 0.029s
    
    OK


### Features
- Aggregate tests recursively in a directory matching the
  pattern ``test_*.yml`` using the commandline tool
  ``climactic``
- Compare stdout, directory structure, and file contents
  against expected string values
- Tests are run in a temporary directory to avoid data loss
  and path-dependent results
- Set environment variables per-test with the ``env`` task
- ``bash``-like ``${VAR}`` substitution for input commands
  and output validation
- Compatibility with the standard ``unittest`` package


#### Commands

The top-level of a climactic test file describes a list of
commands. Commands are executed in order (unless specified as a
dictionary, in which case execution order is undefined, but
each is still executed).

The following commands are currently supported.

##### Action Commands (shell interaction)

- **env**:
  sets environment variables which can be used in ``run``
  commands and assertions
  
- **run**:
  runs one or more commands; nearly acts like a bash script
  (performs environment variable substitution)

- **write-file-utf8**:
  writes a string to a file

##### Assertion Commands (test conditions)

- **assert-output**:
  compares the output of the most recent ``run`` command
  with an expected variable (performs environment variable
  substitution)

- **assert-tree**:
  compares the directory structure of the directory being
  tested against an expected structure

- **assert-file-utf8**:
  compares the contents of a file against an expected
  string


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


## Usage Examples

The following should work out of the box if you opted to
install from source (and, for example, cloned the source tree
to ``~/climactic``):

    ~$ cd climactic
    ~/climactic$ climactic examples -v 1
    ..
    ----------------------------------------------------------------------
    Ran 2 tests in 0.016s

    OK
    
    ~/climactic$ climactic examples -v 2
    examples/test_hello.yml ... ok
    examples/git/test_init.yml ... ok
    
    ----------------------------------------------------------------------
    Ran 2 tests in 0.017s

    OK


To begin exploring all of the features of ``climactic``,
create a new directory and add the test file
``test_git_init.yml``:

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


Now run ``climactic``:

    .
    ----------------------------------------------------------------------
    Ran 1 test in 0.029s
    
    OK


## Contributing

 * Please do!
 * In my personal projects, I usually use a narrow line width of
 80 characters because I like to review code on my phone or tablet;
 this is a loose standard, but there is a greater probability of
 getting your pull request accepted if you adopt it :)


## Author

[Brian Jorgensen](brian.jorgensen+climactic@gmail.com)

[LinkedIn](https://www.linkedin.com/in/briangregoryjorgensen)


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

# ...

*Don't Take Any Wooden Nickels*
