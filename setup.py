PROJECT_URL = 'https://github.com/b33j0r/climactic'
PROJECT_VERSION = '0.1.1'


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
    description='YAML-based tests for command-line utilities',
    long_description=read('README.md'),
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
