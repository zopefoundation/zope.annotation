##############################################################################
#
# Copyright (c) 2001, 2002 Zope Corporation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.0 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Attribute Annotations implementation 

$Id: attribute.py,v 1.1 2004/03/13 23:00:39 srichter Exp $
"""
from BTrees.OOBTree import OOBTree
from interfaces import IAnnotations, IAttributeAnnotatable
from zope.proxy import removeAllProxies
from zope.interface import implements
from zope.app.location.interfaces import ILocation

class AttributeAnnotations:
    """Store annotations in the __annotations__ attribute on a
       'IAttributeAnnotatable' object.
    """
    implements(IAnnotations)
    __used_for__ = IAttributeAnnotatable

    def __init__(self, obj):
        # We could remove all proxies from obj at this point, but
        # for now, we'll leave it to users of annotations to do that.
        # Users of annotations will typically need to do their own
        # unwrapping anyway.

        self.wrapped_obj = obj
        self.unwrapped_obj = removeAllProxies(obj)

    def __getitem__(self, key):
        """See zope.app.annotation.interfaces.IAnnotations"""
        annotations = getattr(self.unwrapped_obj, '__annotations__', None)
        if annotations is None:
            raise KeyError, key
        return annotations[key]

    def __setitem__(self, key, value):
        """See zope.app.annotation.interfaces.IAnnotations"""
        if ILocation.providedBy(value):
            value.__parent__ = self.unwrapped_obj

        try:
            annotations = self.unwrapped_obj.__annotations__
        except AttributeError:
            annotations = self.unwrapped_obj.__annotations__ = OOBTree()

        annotations[key] = value

    def __delitem__(self, key):
        """See zope.app.interfaces.annotation.IAnnotations"""
        try:
            del self.unwrapped_obj.__annotations__[key]
        except AttributeError:
            raise KeyError, key

    def get(self, key, default=None):
        """See zope.app.annotation.interfaces.IAnnotations"""
        try:
            return self.unwrapped_obj.__annotations__.get(key, default)
        except AttributeError:
            # I guess default shouldn't be wrapped.
            return default

    def __getattr__(self, name):
        # this method is for getting methods and attributes of the
        # mapping object used to store annotations.
        try:
            attr = getattr(self.unwrapped_obj.__annotations__, name)
        except AttributeError:
            if not hasattr(self.unwrapped_obj, '__annotations__'):
                annotations = self.unwrapped_obj.__annotations__ = OOBTree()
                attr = getattr(annotations, name)
            else:
                raise
            
        return attr
