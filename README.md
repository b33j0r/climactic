# ``climactic``

## [See the Project Documentation at ReadTheDocs.org](http://climactic.readthedocs.org/en/latest)

*Testing commandline utilities*

A simple testing framework for running
shell commands and verifying their behavior. Tests are
written as YAML files which specify the commands to run
along with assertions about the output (currently, stdout
and file/directory contents).

It is written in Python 3, but it can be used for testing
any kind of shell-based application using just the
`climactic` utility and your test files (by default,
files matching `**/test_*.yml`).


**NOTE: ``climactic`` is a Python 3.4+ package**


### Hello, World!

So, what does this actually look like? We try to keep it simple.

``test_hello.yml``:

    ---
    # A very simple test!
    
    - run: >
        echo Hello world!
    
    - assert-output: >
        Hello world!

Run the `climactic` test runner:

    ~$ climactic test_hello.yml
    .
    ----------------------------------------------------------------------
    Ran 1 test in 0.029s
    
    OK

If you want to use it with existing unit tests via `py.test`:

    ~/climacticpytest$ py.test
    ================= test session starts ==================
    platform darwin -- Python 3.4.2 -- py-1.4.28 -- pytest-2.7.1
    rootdir: /Users/brjorgensen/climacticpytest/climacticpytest, inifile:
    plugins: climactic
    collected 2 items
    
    test_hello.yml .
    test_other_thing.py .
    
    =============== 2 passed in 0.01 seconds ===============

### Features
- Pytest integration
- Aggregate tests recursively in a directory matching the
  pattern ``test_*.yml`` using the commandline tool
  ``climactic``
- Compare stdout, directory structure, and file contents
  against expected string values
- Tests are run in a temporary directory to avoid data loss
  and path-dependent results
- Set environment variables per-test with the ``env``
  command
- ``bash``-like ``${VAR}`` substitution for input commands
  and output validation
- Compatibility with the standard ``unittest`` package


## Install

``climactic`` is registered in PyPI, so you can use pip:

    pip install climactic

Or (not necessary if you aren't using `py.test`, or already
have an up-to-date `pytest`):

    pip install climactic[pytest]

To use the most recent source code:

    virtualenv -p python3 climactic_venv
    source climactic_venv/bin/activate
    pip install -U -e git+https://github.com/b33j0r/climactic.git#egg=climactic

Either method will install the ``climactic`` python package
as well as the ``climactic`` commandline utility.


#### Commands

The top-level of a climactic test file describes a list of
commands. Commands are executed in order (unless specified as a
dictionary, in which case execution order is undefined, but
each is still executed).

The following commands are currently supported:

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


## Usage Examples

The following should work out of the box if you opted to
install from source (and, for example, cloned the source tree
to ``~/climactic``):

    ~$ cd climactic
    ~/climactic$ climactic examples -v 1
    ...
    ----------------------------------------------------------------------
    Ran 3 tests in 0.016s

    OK

When tests begin to get into the dozens or hundreds (and that
one random one breaks or becomes slow for some reason), it can
be nice to see which ones are running and when. For this purpose,
we can specify ``--verbosity`` or its shortcut, ``-v``:

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
([LinkedIn](https://www.linkedin.com/in/briangregoryjorgensen))


## License

- Copyright (C) 2015  Brian Jorgensen
- (Submit a pull request for Your Name Here)

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
