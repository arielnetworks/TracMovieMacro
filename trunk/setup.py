#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup

try:
    long_description = ''.join([
        open('README.md').read(),
        open('changelog').read(),
    ])
except:
    long_description = ''

setup(
    name='TracMovieMacro',
    version='0.3',
    description='Safely embed various movies into wiki pages',
    long_description=long_description,
    packages=['movie'],
    package_data={
        'movie': [
            'htdocs/img/*.jpg',
            'htdocs/js/*.js',
            'htdocs/js/skin/*.css',
            'htdocs/js/skin/img/*',
            'htdocs/swf/*.swf',
        ],
    },
    author='Louis Cordier',
    author_email='lcordier@gmail.com',
    maintainer='Tetsuya Morimoto',
    maintainer_email='tetsuya dot morimoto at gmail dot com',
    url='http://trac-hacks.org/wiki/MovieMacro/',
    license='BSD',
    keywords='trac plugin movie video html5 macro',
    platforms=['unix', 'linux', 'osx', 'cygwin', 'win32'],
    install_requires=['Trac >= 0.12'],
    classifiers=[
        'Framework :: Trac',
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'License :: OSI Approved :: BSD License',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development',
    ],
    entry_points={
        'trac.plugins': [
            'movie.macro = movie.macro',
            'movie.web_ui = movie.web_ui',
        ],
    },
)
