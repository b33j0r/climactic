# ``climactic``

*Testing commandline utilities*

A simple testing framework for running
shell commands and verifying their behavior. Tests are
written as YAML files which specify the commands to run
along with assertions about the output (currently, stdout
and file/directory contents).

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
- Set environment variables per-test with the ``env``
  command
- ``bash``-like ``${VAR}`` substitution for input commands
  and output validation
- Compatibility with the standard ``unittest`` package


## Install

Let's just go ahead and do this--at some point you'll be
glad you did :p

To use the most recent source code (recommended at this time,
as development is very active):

    virtualenv -p python3 climactic_venv
    source climactic_venv/bin/activate
    pip install -U -e git+https://github.com/b33j0r/climactic.git#egg=climactic

``climactic`` is registered in PyPI, so pip works too:

    pip install climactic

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
    ..
    ----------------------------------------------------------------------
    Ran 2 tests in 0.016s

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


## Historical Notes

This project was created on June 4, 2015. It was created in the
context of "how do I test a command-line utility in a concise
yet expressive manner?"

The YAML syntax is inspired by the author seeing successful
applications of ansible and docker. Yet, there are a few small
inconsistencies which deserve some explanation...

#### Command vs. Task

tl;dr: You probably only need to know this if you uncover a
defect, contribute a pull request, or fork the repository.
But hey, I documented it! ``--BJ 06/07/15``

A lot of what we do as coders is come up with names for our
constructs. I plan to define these terms more narrowly in
the near future, but here is the current state of things
in this codebase:

**task**: input that is specified in parallel within an
          associative array (``dict``):

    do_this: ...
    do_this_maybe_before_or_after: ...

**command**: input that is specified in an ordered array
             (``list``):
    
    - do_the_first_thing
        parameter_a: ...
        parameter_b: ...
        ...
    - do_the_second_thing
        ...

From a design perspective, everything that results in the
instantiation of a ``Command`` object will eventually have a
sensible name. But at this moment, you might see a bit of this.

The ambiguity arises from the flexible structure of YAML. I am
open to suggestions; I hadn't thought about it much until I
noticed after release that the mix of the terms *task* and
*command* was a bit confusing.


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
