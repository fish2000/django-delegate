#/usr/bin/env python
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import delegate

setup(
    name='django-delegate',
    version='%s.%s.%s' % delegate.__version__,
    description='Automatic delegate methods for Django managers and querysets without runtime dispatch penalties.',
    author=delegate.__author__,
    author_email='fish2000@gmail.com',
    maintainer=delegate.__author__,
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
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Utilities'
    ]
)

