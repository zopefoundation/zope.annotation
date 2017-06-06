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

from zope.testing import cleanup
from zope.interface import implementer
from zope.annotation.attribute import AttributeAnnotations
from zope.annotation.interfaces import IAttributeAnnotatable

from zope.annotation.tests.annotations import AnnotationsTestBaseMixin

class AttributeAnnotationsTest(AnnotationsTestBaseMixin, unittest.TestCase):

    def setUp(self):

        cleanup.setUp()

        @implementer(IAttributeAnnotatable)
        class Dummy(object):
            pass

        self.obj = Dummy()
        self.annotations = AttributeAnnotations(self.obj)

    def tearDown(self):
        cleanup.tearDown()

    def test_two_annotations_same_obj_set(self):
        annotations2 = AttributeAnnotations(self.obj)

        # Initially both are empty
        self.assertFalse(self.annotations)
        self.assertFalse(annotations2)

        # Adding a key is initially only visible in the direct object
        self.annotations['key'] = 42
        self.assertIn('key', self.annotations)
        self.assertNotIn('key', annotations2)

        self.annotations['key2'] = 43
        self.assertIn('key2', self.annotations)
        self.assertNotIn('key2', annotations2)

        # But manipulating the alternate object via adding an item
        # refreshes the annotations
        annotations2['key3'] = 44
        self.assertIn('key', self.annotations)
        self.assertIn('key', annotations2)
        self.assertIn('key2', self.annotations)
        self.assertIn('key2', annotations2)
        self.assertIn('key3', self.annotations)
        self.assertIn('key3', annotations2)

    def test_two_annotations_same_obj_del(self):
        annotations2 = AttributeAnnotations(self.obj)

        # Initially both are empty
        self.assertFalse(self.annotations)
        self.assertFalse(annotations2)

        # Adding a key is initially only visible in the direct object
        self.annotations['key'] = 42
        self.assertIn('key', self.annotations)
        self.assertNotIn('key', annotations2)

        self.annotations['key2'] = 43
        self.assertIn('key2', self.annotations)
        self.assertNotIn('key2', annotations2)

        # But manipulating the alternate object via deleting an item
        # refreshes the annotations
        del annotations2['key']
        self.assertNotIn('key', self.annotations)
        self.assertNotIn('key', annotations2)
        self.assertIn('key2', self.annotations)
        self.assertIn('key2', annotations2)

    def test_two_annotations_same_obj_create_after_modify(self):
        self.annotations['key'] = 42

        # Creating a new attribute annotations at this time recognizes
        # the key
        annotations2 = AttributeAnnotations(self.obj)
        self.assertIn('key', annotations2)
        self.assertEqual(42, annotations2['key'])


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
