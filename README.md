# ``climactic``

*Testing command-line utilities*


## Install

Most simply:

    pip install climactic


## Usage

Create a test file, for example, ``test_git_init.yml``:

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
