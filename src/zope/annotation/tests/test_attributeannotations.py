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
import unittest

from zope.interface import implementer

from zope.annotation.attribute import AttributeAnnotations
from zope.annotation.interfaces import IAttributeAnnotatable
from zope.annotation.tests.annotations import AnnotationsTestBase


class AttributeAnnotationsTest(AnnotationsTestBase, unittest.TestCase):

    def setUp(self):
        from zope.testing import cleanup

        cleanup.setUp()

        @implementer(IAttributeAnnotatable)
        class Dummy:
            pass

        self.obj = Dummy()
        self.annotations = AttributeAnnotations(self.obj)

    def tearDown(self):
        from zope.testing import cleanup
        cleanup.tearDown()

    def testInterfaceVerifies(self):
        super().testInterfaceVerifies()
        self.assertIs(self.obj, self.annotations.__parent__)

    def testMigration(self):
        obj = self.obj
        obj.__annotations__ = dict(a=1)
        od = obj.__dict__
        annotations = AttributeAnnotations(obj)
        self.assertEqual(annotations["a"], 1)
        self.assertNotIn("__annotations__", od)

    def testTypeHints(self):

        @implementer(IAttributeAnnotatable)
        class WithTypeHints:
            a: int

        obj = WithTypeHints()
        hints = obj.__annotations__
        annotations = AttributeAnnotations(obj)
        self.assertFalse(annotations)
        annotations["a"] = 1
        self.assertEqual(annotations["a"], 1)
        self.assertIs(obj.__annotations__, hints)

    def test_notification(self):
        from copy import copy

        class Counter:
            c = 0

            def __call__(self, unused):
                self.c += 1

        counter = Counter()

        class NotifyingAttributeAnnotations(AttributeAnnotations):
            notify_object_changed = counter

        # initial annotation
        obj = copy(self.obj)
        ann = NotifyingAttributeAnnotations(obj)
        self.assertEqual(counter.c, 0)
        ann["x"] = 1
        self.assertEqual(counter.c, 1)

        # migration
        obj = copy(self.obj)
        obj.__annotations__ = dict(a=1)
        ann = NotifyingAttributeAnnotations(obj)
        self.assertEqual(counter.c, 2)


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
