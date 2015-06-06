from setuptools import setup

PROJECT_URL = 'https://github.com/b33j0r/climactic'
PROJECT_VERSION = '0.1.0'

setup(
    name='climactic',
    version=PROJECT_VERSION,
    packages=[
        'climactic'
    ],
    url=PROJECT_URL,
    download_url=PROJECT_URL + '/tarball/' + PROJECT_VERSION,
    license='GPLv2',
    author='Brian Jorgensen',
    author_email='brian.jorgensen@gmail.com',
    description='YAML-based test framework for '
                'command-line utilities',
    keywords=['testing', 'cli', 'yaml', 'unittest']
)
