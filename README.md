# ``climactic``

*YAML-based test framework for command-line utilities*

    ---
    # Run `git init` and verify that the expected directory
    # structure and file contents are produced.
    
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

GPLv2

## Author

[Brian Jorgensen](brian.jorgensen@gmail.com)

*Don't Take Any Wooden Nickels*
