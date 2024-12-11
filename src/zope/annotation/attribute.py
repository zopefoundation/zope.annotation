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
from collections.abc import MutableMapping as DictMixin
from weakref import WeakKeyDictionary


try:
    from BTrees.OOBTree import OOBTree as _STORAGE
except ImportError:  # pragma: no cover
    logging.getLogger(__name__).warning(
        'BTrees not available: falling back to dict for attribute storage')
    _STORAGE = dict

from zope import component
from zope import interface
from zope.annotation import interfaces


_EMPTY_STORAGE = _STORAGE()

ATTR = "_zope_annotations"


@interface.implementer(interfaces.IAnnotations)
@component.adapter(interfaces.IAttributeAnnotatable)
class AttributeAnnotations(DictMixin):
    """Store annotations on an object

    Store annotations in the attribute given by ``ATTR`` on a
    `IAttributeAnnotatable` object.
    """

    # optional callback to notify that the object was changed
    # can be used e.g. to inform ``plone.protect``
    notify_object_changed = None

    # Yes, there's a lot of repetition of the `getattr` call,
    # but that turns out to be the most efficient for the ways
    # instances are typically used without sacrificing any semantics.
    # See https://github.com/zopefoundation/zope.annotation/issues/8
    # for a discussion of alternatives (which included functools.partial,
    # a closure, capturing the annotations in __init__, and versions
    # with getattr and exceptions).

    def __init__(self, obj, context=None):
        self.obj = obj
        if getattr(obj, ATTR, None) is None:
            # check for migration
            ann = getattr(obj, "__annotations__", None)
            if ann is not None and _check_ann(obj, ann):
                # migrate
                setattr(obj, ATTR, ann)
                delattr(obj, "__annotations__")
                if self.notify_object_changed is not None:
                    self.notify_object_changed(obj)

    @property
    def __parent__(self):
        return self.obj

    def __bool__(self):
        return bool(getattr(self.obj, ATTR, 0))

    def get(self, key, default=None):
        """See zope.annotation.interfaces.IAnnotations"""
        annotations = getattr(self.obj, ATTR, _EMPTY_STORAGE)
        return annotations.get(key, default)

    def __getitem__(self, key):
        annotations = getattr(self.obj, ATTR, _EMPTY_STORAGE)
        return annotations[key]

    def keys(self):
        annotations = getattr(self.obj, ATTR, _EMPTY_STORAGE)
        return annotations.keys()

    def __iter__(self):
        annotations = getattr(self.obj, ATTR, _EMPTY_STORAGE)
        return iter(annotations)

    def __len__(self):
        annotations = getattr(self.obj, ATTR, _EMPTY_STORAGE)
        return len(annotations)

    def __setitem__(self, key, value):
        """See zope.annotation.interfaces.IAnnotations"""
        try:
            annotations = getattr(self.obj, ATTR)
        except AttributeError:
            annotations = _STORAGE()
            setattr(self.obj, ATTR, annotations)
            if self.notify_object_changed is not None:
                self.notify_object_changed(self.obj)

        annotations[key] = value

    def __delitem__(self, key):
        """See zope.app.interfaces.annotation.IAnnotations"""
        try:
            annotation = getattr(self.obj, ATTR)
        except AttributeError:
            raise KeyError(key)

        del annotation[key]


_with_annotations_slot = WeakKeyDictionary()


def _check_ann(obj, ann):
    """check whether *ann* is an annotation on *obj*.

    We assume ``obj.__annotations__ is ann is not None``.
    """
    # *ann* can come from *obj* itself or its class of one of the base classes
    # we check whether it comes from *obj* itself
    try:
        if obj.__dict__["__annotations__"] is ann:
            return True
    except (AttributeError, KeyError):
        pass
    # it does not come from *obj.__dict__"
    # it may come from an ``__annotations__`` slot
    oc = obj.__class__
    if oc not in _with_annotations_slot:
        _with_annotations_slot[oc] = \
            any("__annotations__" in c.__dict__.get("__slots__", ())
                for c in oc.__mro__)
    # even without ``__annotations__`` slot, it may still
    # come from *obj* (mediated by some weird descriptor)
    # but we ignore this case
    return _with_annotations_slot[oc]
