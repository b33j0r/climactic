#! /usr/bin/env python
import ez_setup
ez_setup.use_setuptools()


import os
from setuptools import setup


DIRECTORY = os.path.dirname(__file__)
REQUIREMENT_FILE_EXTENSION = '.txt'


from climactic import (
    PROJECT_URL,
    PROJECT_VERSION,
    PROJECT_DESCRIPTION,
    PROJECT_LONG_DESCRIPTION
)

def read_requirements(path):
    """Return a list of requirements from the file at the given path."""
    result = []
    if os.path.isfile(path):
        with open(path) as f:
            result.append(f.read())
    return result


def dependency_links():
    path = os.path.join(DIRECTORY, 'requirements',
                        'dependency_links' + REQUIREMENT_FILE_EXTENSION)
    return read_requirements(path)


def install_requires():
    path = os.path.join(DIRECTORY, 'requirements',
                        'runtime' + REQUIREMENT_FILE_EXTENSION)
    result = read_requirements(path)
    path = os.path.join(DIRECTORY, 'requirements',
                        'runtime_via_links' + REQUIREMENT_FILE_EXTENSION)
    return result + read_requirements(path)


def extras_require():
    result = {}
    extras_dir = os.path.join(DIRECTORY, 'requirements', 'extras')
    if os.path.isdir(extras_dir):
        for extra in os.listdir(extras_dir):
            if not extra.endswith(REQUIREMENT_FILE_EXTENSION):
                continue
            path = os.path.join(extras_dir, extra)
            extra = extra[:-len(REQUIREMENT_FILE_EXTENSION)]
            result[extra] = read_requirements(path)
    return result

setup(
    name='climactic',
    version=PROJECT_VERSION,
    packages=[
        'climactic',
        'climactic.test',
        'climactic.plugins'
    ],
    url=PROJECT_URL,
    download_url=PROJECT_URL + '/tarball/v' + PROJECT_VERSION,
    license='GPLv2',
    author='Brian Jorgensen',
    author_email='brian.jorgensen@gmail.com',
    description=PROJECT_DESCRIPTION,
    long_description=PROJECT_LONG_DESCRIPTION,
    keywords=[
        'testing',
        'cli',
        'yaml',
        'unittest'
    ],
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
    entry_points={
        'console_scripts': [
            'climactic=climactic.cli:main',
            'json-env=climactic.cli:json_env'
        ],
        'pytest11': [
            'pytest-climactic=climactic.plugins.pytest'
        ]
    },
    dependency_links=dependency_links(),
    install_requires=install_requires(),
    extras_require=extras_require(),
)
