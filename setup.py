#! /usr/bin/env python
import os

from setuptools import setup

from climactic import (
    PROJECT_URL,
    PROJECT_VERSION,
    PROJECT_DESCRIPTION,
    PROJECT_LONG_DESCRIPTION
)


project_dir = os.path.dirname(__file__)


def read(rel_path):
    return open(
        os.path.join(project_dir, rel_path)
    ).read()


setup(
    name='climactic',
    version=PROJECT_VERSION,
    packages=[
        'climactic',
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
            'climactic=climactic.cli:main'
        ],
        'pytest11': [
            'pytest-climactic=climactic.plugins.pytest'
        ]
    },
    install_requires=[
        "PyYAML==3.11"
    ],
    extras_require={
        'pytest': [
            "pytest>=2.7.1"
        ]
    }
)
