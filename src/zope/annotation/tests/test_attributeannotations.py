##############################################################################
#
# Copyright (c) 2001, 2002 Zope Foundation and Contributors.
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
"""Tests the 'AttributeAnnotations' adapter. Also test the annotation
factory.
"""
import unittest

from zope.annotation.tests.annotations import AnnotationsTestBase

class AttributeAnnotationsTest(AnnotationsTestBase,
                               unittest.TestCase,
                              ):
    def setUp(self):
        from zope.testing import cleanup
        from zope.interface import implementer
        from zope.annotation.attribute import AttributeAnnotations
        from zope.annotation.interfaces import IAttributeAnnotatable

        cleanup.setUp()

        @implementer(IAttributeAnnotatable)
        class Dummy(object):
            pass

        self.annotations = AttributeAnnotations(Dummy())

    def tearDown(test=None):
        from zope.testing import cleanup
        cleanup.tearDown()


def setUp(test=None):
    from zope.component import provideAdapter
    from zope.annotation.attribute import AttributeAnnotations
    provideAdapter(AttributeAnnotations)

def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(AttributeAnnotationsTest),
    ))
