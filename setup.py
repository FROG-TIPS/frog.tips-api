#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

version = '1.0.6-DEV'

setup(
    name='frog',
    packages=find_packages("src"),
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=False,
    version=version,
    description='FROG TIPS FOR ALL',
    author='FROG SYSTEMS',
    classifiers=[
        'Private',
    ],
    install_requires=[
        'flask == 0.10.1',
        'flask-sqlalchemy == 2.1',
        'pyasn1 == 0.1.9',
        'jsonpatch == 1.14',
        'enum34 == 1.1.6',
        'howabout == 1.1.0',
    ],
    license='Private',
)
