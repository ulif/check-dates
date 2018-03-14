#!/usr/bin/env python
import ast
import email.utils
import os
import re
from setuptools import setup

here = os.path.dirname(__file__)

with open(os.path.join(here, 'README.rst')) as readme:
    with open(os.path.join(here, 'CHANGES.rst')) as changelog:
        long_description = readme.read() + '\n\n' + changelog.read()

metadata = {}
with open(os.path.join(here, 'check_dates.py')) as f:
    rx = re.compile('(__version__|__author__|__url__|__license__) = (.*)')
    for line in f:
        m = rx.match(line)
        if m:
            metadata[m.group(1)] = ast.literal_eval(m.group(2))
version = metadata['__version__']
author, author_email = email.utils.parseaddr(metadata['__author__'])
url = metadata['__url__']
license = metadata['__license__']

setup(
    name='check-dates',
    version=version,
    author=author,
    author_email=author_email,
    url=url,
    description='Check manpage dates in a Python source package',
    long_description=long_description,
    keywords=['distutils', 'setuptools', 'packaging', 'dates', 'checker',
              'linter'],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: '
        'GNU General Public License v3 or later (GPL v3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
    license=license,

    py_modules=['check_dates'],
    zip_safe=False,
    install_requires=[],
    extras_require={
        'test': ['pytest'],
    },
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'check-dates= check_dates:main',
        ],
    },
)
