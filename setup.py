#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


def parse_requirements(requirements):
    with open(requirements) as f:
        return [l.strip('\n') for l in f if l.strip('\n') and not l.startswith('#')]


with open('README.md') as f:
    long_description = f.read().strip()

test_requirements = parse_requirements('test-requirements.txt')

setup(
    name='pyuri',
    packages=find_packages(exclude=('tests.*', 'tests',)),
    url='https://github.com/nick-allen/pyuri',
    license='MIT',
    author='Nick Allen',
    author_email='nick.allen.cse@gmail.com',
    description='Better URI Handling',
    long_description=long_description,
    include_package_data=True,
    zip_safe=False,
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    extras_require={
        'test': test_requirements
    },
    test_suite='nose.collector',
    tests_require=test_requirements
)
