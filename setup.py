#!/usr/bin/env python
import os
from setuptools import setup, find_packages


README = os.path.join(os.path.dirname(__file__), 'README.md')

# When running tests using tox, README.md is not found
try:
    with open(README) as file:
        long_description = file.read()
except Exception:
    long_description = ''


setup(
    name='skyapi',
    version='0.0.1',
    description='A python client for v1 of Blackbaud SKY API',
    long_description=long_description,
    url='https://github.com/jpipas/python-sky-api',
    author='Jeff Pipas',
    author_email='jpipas@gmail.com',
    license='MIT',
    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
    ],
    keywords='blackbuad sky api client wrapper',
    packages=find_packages(),
    install_requires=['requests>=2.7.0'],
    # test_suite='tests',
)
