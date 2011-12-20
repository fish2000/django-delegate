#/usr/bin/env python
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import sys, os
sys.path.append(os.getcwd())

import version

setup(
    name='django-delegate',
    version='%s.%s.%s' % version.__version__,
    description='Automatic delegate methods for Django managers and querysets without runtime dispatch penalties.',
    author=version.__author__,
    author_email='fish2000@gmail.com',
    maintainer=version.__author__,
    maintainer_email='fish2000@gmail.com',
    license='BSD',
    url='http://github.com/fish2000/django-delegate/',
    keywords=[
        'django',
        'delegate',
        'queryset',
        'manager',
        'method',
        'dispatch',
        'syntax-sugar',
    ],
    packages=[
        'delegate',
    ],
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
        'Topic :: Database',
        'Topic :: Utilities',
    ]
)

