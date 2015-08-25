#!/usr/bin/env python

from distutils.core import setup

setup(name='Googleapihelper',
      version='0.1',
      description='Wrapper around googleapiclient',
      author='Andrew Tergis',
      author_email='theterg@gmail.com',
      packages=['googleapihelper'],,
      dependencies=['google-api-python-client','oauth2client']
     )
