PROJECT_URL = 'https://github.com/b33j0r/climactic'
PROJECT_VERSION = '0.1.1'
PROJECT_DESCRIPTION = """
YAML-based tests for commandline utilities
""".strip()
PROJECT_LONG_DESCRIPTION = """
A simple testing framework for running
shell commands and verifying their behavior. Tests are
written as YAML files which specify the commands to run
along with assertions about the output (currently, stdout
and file/directory contents).

* NOTE: climactic is a Python 3 package

Features
- Aggregate tests recursively in a directory matching the
  pattern "test_*.yml" using the commandline tool
  `climactic`
- Compatibility with the standard `unittest` package
- Tests are run in a temporary directory to avoid data loss
  and path-dependent results
- Set environment variables per-test with the 'env' task
- Compare stdout, directory structure, and file contents
  to expected string values
- bash-like ${VAR} substitution for input commands
  and output validation
""".strip()

import os
from setuptools import setup


project_dir = os.path.dirname(__file__)


def read(rel_path):
    return open(
        os.path.join(project_dir, rel_path)
    ).read()


def read_requirements():
    return [
        p.strip() for p in read(
            "requirements.txt"
        ).split("\n") if p.strip()
    ]


setup(
    name='climactic',
    version=PROJECT_VERSION,
    packages=[
        'climactic'
    ],
    url=PROJECT_URL,
    download_url=PROJECT_URL + '/tarball/v' + PROJECT_VERSION,
    license='GPLv2',
    author='Brian Jorgensen',
    author_email='brian.jorgensen@gmail.com',
    description=PROJECT_DESCRIPTION,
    long_description=PROJECT_LONG_DESCRIPTION,
    install_requires=read_requirements(),
    keywords=['testing', 'cli', 'yaml', 'unittest'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "Topic :: Software Development :: Testing",
        "License :: OSI Approved"
        " :: GNU General Public License v2 (GPLv2)",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"

    ],
    scripts=[
        "bin/climactic"
    ]
)
