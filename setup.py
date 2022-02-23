#!/usr/bin/env python

import sys
from setuptools import setup, find_packages


setup(
    name="pfourchan-dl",
    version="0.1",
    description="A simple Imageboard Threads downloader",
    author="Eduardo Macedo",
    author_email="dudmacedo@gmail.com",
    url="https://github.com/dudmacedo/pfourchan-dl",
    packages=find_packages(),
    namespace_packages=['pfourchan-dl.plugins']
)