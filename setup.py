#/usr/bin/env python
# encoding: utf-8
from __future__ import print_function

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import sys
import os
sys.path.append(os.getcwd())

import version

if 'sdist' in sys.argv and 'upload' in sys.argv:
    import commands
    finder = "/usr/bin/find %s \( -name \*.pyc -or -name .DS_Store \) -delete"
    theplace = os.getcwd()
    if theplace not in (".", "/"):
        print("+ Deleting crapola from %s..." % theplace)
        print("$ %s" % finder % theplace)
        commands.getstatusoutput(finder % theplace)
        print("")

setup(
    name='django-delegate',
    version='%s.%s.%s' % version.__version__,
    description=version.__doc__,
    long_description=version.__doc__,
    author=version.__author__,
    author_email=version.__email__,
    maintainer=version.__author__,
    maintainer_email=version.__email__,
    license='BSD',
    url='http://github.com/fish2000/django-delegate/',
    download_url='https://github.com/fish2000/django-delegate/zipball/master',
    keywords=[
        'django',
        'delegate',
        'queryset',
        'manager',
        'method',
        'dispatch',
        'syntax-sugar'],
    packages=[
        'delegate'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Environment :: Other Environment',
        'Environment :: Plugins',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Programming Language :: Python :: Implementation :: Jython',
        'Topic :: Database',
        'Topic :: Utilities']
)

