# ``climactic``

*Testing command-line utilities*


## Install

Most simply:

    pip install climactic


## Usage

### ``test_init.yml``

    ---
    # Run `git init` and verify that
    # the expected directory structure
    # and file contents are produced.
    
    - env:
        CMD: git
    
    - run: |
        ${CMD} init
    
    - assert-tree:
      - .git:
        - HEAD
        - objects:
        - refs:
          - heads:
          - tags:
    
    - assert-file-utf8:
      - .git/HEAD: |
          refs/origin/master


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
