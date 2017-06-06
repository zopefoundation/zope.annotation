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
"""Attribute Annotations implementation"""
import logging

try:
    from BTrees.OOBTree import OOBTree as _STORAGE
except ImportError: # pragma: no cover
    logging.getLogger(__name__).warning(
        'BTrees not available: falling back to dict for attribute storage')
    _STORAGE = dict

from zope import component, interface
from zope.annotation import interfaces

from collections import MutableMapping as DictMixin

_EMPTY_STORAGE = _STORAGE()

@interface.implementer(interfaces.IAnnotations)
@component.adapter(interfaces.IAttributeAnnotatable)
class AttributeAnnotations(DictMixin):
    """Store annotations on an object

    Store annotations in the `__annotations__` attribute on a
    `IAttributeAnnotatable` object.
    """

    def __init__(self, obj, context=None):
        self.obj = obj
        self._annotations = getattr(obj, '__annotations__', _EMPTY_STORAGE)

    def __bool__(self):
        return bool(self._annotations)

    __nonzero__ = __bool__

    def get(self, key, default=None):
        """See zope.annotation.interfaces.IAnnotations"""
        return self._annotations.get(key, default)

    def __getitem__(self, key):
        return self._annotations[key]

    def keys(self):
        return self._annotations.keys()

    def __iter__(self):
        return iter(self._annotations)

    def __len__(self):
        return len(self._annotations)

    # Writing must refresh the attribute from the underlying object,
    # in case of modification by a different AttributeAnnotations object.

    def __setitem__(self, key, value):
        """See zope.annotation.interfaces.IAnnotations"""
        try:
            self._annotations = self.obj.__annotations__
        except AttributeError:
            self._annotations = self.obj.__annotations__ = _STORAGE()

        self._annotations[key] = value

    def __delitem__(self, key):
        """See zope.app.interfaces.annotation.IAnnotations"""
        try:
            self._annotations = self.obj.__annotations__
        except AttributeError:
            raise KeyError(key)

        del self._annotations[key]
