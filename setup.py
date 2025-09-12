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

from setuptools import setup


def read(*rnames):
    with open(os.path.join(os.path.dirname(__file__), *rnames)) as f:
        return f.read()


tests_require = [
    'zope.component[zcml]',
    'zope.configuration',
    'zope.testing',
    'zope.testrunner >= 6.4',
]

setup(
    name='zope.annotation',
    version='6.0',
    url='https://github.com/zopefoundation/zope.annotation',
    license='ZPL-2.1',
    description='Object annotation mechanism',
    author='Zope Foundation and Contributors',
    author_email='zope-dev@zope.dev',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Zope Public License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development',
    ],
    keywords='zope annotation ZODB zope3 ztk',
    long_description=(
        read('README.rst')
        + '\n\n' +
        read('CHANGES.rst')),
    python_requires='>=3.9',
    install_requires=[
        'setuptools',
        'zope.interface',
        'zope.component',
        'zope.location',
        'zope.proxy',
    ],
    extras_require=dict(
        btrees=[
            'BTrees',
            'persistent',
        ],
        docs=[
            'Sphinx',
            'repoze.sphinx.autointerface',
        ] + tests_require,
        test=tests_require,
        testing=tests_require + ['nose', 'coverage'],
        zcml=[
            'zope.component[zcml]',
            'zope.configuration',
        ],
    ),
    include_package_data=True,
    zip_safe=False,
)
