#!/usr/bin/env python3

from distutils.core import setup

setup(name='Markov',
      version='1.3',
      description='Markov Text Generation',
      author='Pedro Melgueira',
      author_email='pm@pedromelgueira.com',
      py_modules=['markov'],
      install_requires=['numpy==1.21.2'])
