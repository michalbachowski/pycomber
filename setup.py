#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup


# monkey patch os.link to force using symlinks
import os
del os.link

setup(name='PyComber',
    url='https://github.com/michalbachowski/pycomber',
    version='0.1.0',
    description='Python configurable object merger',
    license='MIT',
    author='Michał Bachowski',
    author_email='michal@bachowski.pl',
    packages=['pycomber'],
    package_dir={'': 'src'})
