#!/usr/bin/env python

import setuptools
from distutils.core import setup
from setuptools import setup, find_packages

setup(name='uml2dj',
      version='0.0.1',
      description='toold for parse UML 2 and generate django models',
      author='Stas Kridzanovskiy',
      author_email='slaviann@gmail.com',
      packages=find_packages(),
      #install_requires=[
      #    'libxml2',
      #],
      scripts=['bin/uml2dj'],
     )
