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
    }
)
