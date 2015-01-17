#!/usr/bin/python -O
# -*- coding: utf-8 -*-

# Wizards Magic
# Copyright (C) 2011-2014  https://code.google.com/p/wizards-magic/
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

from setuptools import setup
from glob import glob
import py_compile
import os

modules = [
    x
    for x in glob('*.py')
    if x != 'setup.py'
]
print modules
for f in modules:
    os.environ['PYTHONOPTIMIZE'] = "0"
    py_compile.compile(f, f+'c')
    os.environ['PYTHONOPTIMIZE'] = "1"
    py_compile.compile(f, f+'o')

data_files=[
    ('', modules + [f+'c' for f in modules] + [f+'o' for f in modules])
]

for d in ('misc', 'languages'):
    for root, dirs, files in os.walk(d):
        if files:
            data_files.append((root, [os.path.join(root, f) for f in files]))

print data_files

setup(
    name='WizardsMagic',
    version='3.2.21',
    license='GPLv2+',
    description='Wizards Magic - OpenSource Card Game',
    url='https://code.google.com/p/wizards-magic/',
    author='Andrey Pitko',
    author_email='chubakur@gmail.com',

    long_description=(
        'Wizards Magic - OpenSource card game, based on rules of '
        'Magic: The Gathering, written in Python, using Pygame'
    ),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: X11 Applications',
        'Intended Audience :: End Users/Desktop',
        (
            'License :: OSI Approved :: '
            'GNU General Public License v2 or later (GPLv2+)'
        ),
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Games/Entertainment :: Turn Based Strategy'
    ],
    install_requires=['simplejson', 'pygame'],
    requires=['simplejson', 'pygame'],
    data_files=data_files,
    scripts=['WizardsMagic'],
)
