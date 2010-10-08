#!/usr/bin/env python

# ...

from distutils.core import setup

setup(name='web.py-fox',
      version='0.34.13fox-1',
      description='web.py: makes web apps',
      author='Aaron Swartz',
      author_email='me@aaronsw.com',
      maintainer='Branko Vukelic',
      maintainer_email='bg.branko@gmail.com',
      url='http://github.com/foxbunny/webpy',
      packages=['web', 'web.wsgiserver', 'web.contrib'],
      long_description="Poor man's framework bolted onto anti-framework.",
      license="BSD",
      platforms=["any"],
     )
