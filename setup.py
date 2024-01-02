#!/usr/bin/env python

import os
from setuptools import setup, find_packages

DESCRIPTION = 'Strava scrapper'

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

with open(os.path.join(here, 'requirements.txt'), encoding='utf-8') as f:
    requirements = [ x for x in f.read().split('\n') if len(x) > 1 ]

setup(
    python_requires='>=3.5',
    name='strava-scrapper',
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    version=0.1,
    license='GNU',
    author='Maria Garcia',
    author_email='maria.raldua@gmail.com',
    url='https://github.com/Mariag39/strava-scrapper',
    packages=find_packages(),
    classifiers=[
        "License :: OSI Approved :: GNU License",
        "Development Status :: 3 - Alpha",
        "Natural Language :: English",
        "Topic :: Utilities"
    ],
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'scrava = scrava.cli.commands:opening'
        ],
    },
)