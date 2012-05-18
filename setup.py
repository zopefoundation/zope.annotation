##############################################################################
#
# Copyright (c) 2006-2007 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
# This package is developed by the Zope Toolkit project, documented here:
# http://docs.zope.org/zopetoolkit
# When developing and releasing this package, please follow the documented
# Zope Toolkit policies as described by this documentation.
##############################################################################
"""Setup for zope.annotation package
"""

import os
from setuptools import setup, find_packages

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

setup(
    name='zope.annotation',
    version='4.0.0dev',
    url='http://pypi.python.org/pypi/zope.annotation',
    license='ZPL 2.1',
    description='Object annotation mechanism',
    author='Zope Foundation and Contributors',
    author_email='zope-dev@zope.org',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Zope Public License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development',
        ],
    long_description= \
        read('src', 'zope', 'annotation', 'README.txt') 
        + '\n\n' +
        read('CHANGES.txt'),
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['zope',],
    install_requires=['setuptools',
                      'zope.interface',
                      'zope.component',
                      'zope.location',
                      'zope.proxy',
                      'ZODB3',
                      ],
    extras_require=dict(
        test=['zope.testing'],
        zcml=[
            'zope.component[zcml]',
            'zope.configuration',
            ],
        ),
    include_package_data=True,
    zip_safe=False,
    )
