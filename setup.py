#!/usr/bin/env python

from distutils.core import setup

setup(
        name='surly',
        version='0.0.0',
        description='Surly URL Mapper',
        author='Patrick Lawson',
        author_email='patrick.a.lawson@gmail.com',
        url='http://github.com/patricklaw/surly',
        packages=['surly'],
        requires=['nose'],
        classifiers=[
            'Development Status :: 2 - Pre-Alpha',
            'License :: OSI Approved :: Apache Software License',
            'Programming Language :: Python',
        ],
 )
