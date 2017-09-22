Object Annotations
==================

Annotation factories
--------------------

There is more to document about annotations, but we'll just sketch out
a scenario on how to use the annotation factory for now. This is one
of the easiest ways to use annotations -- basically you can see them
as persistent, writable adapters.

.. testsetup::

   from zope.testing import cleanup
   from zope.component import provideAdapter
   from zope.annotation.attribute import AttributeAnnotations
   cleanup.setUp()
   provideAdapter(AttributeAnnotations)

First, let's make a persistent object we can create annotations for:

.. doctest::

   >>> from zope.interface import Interface
   >>> from zope.interface import implementer
   >>> class IFoo(Interface):
   ...     pass
   >>> from zope.annotation.interfaces import IAttributeAnnotatable
   >>> @implementer(IFoo, IAttributeAnnotatable)
   ... class Foo(object):
   ...     pass

We directly say that :class:`Foo` implements
:class:`~zope.annotation.interfacesIAttributeAnnotatable` here. In
practice this is often done in ZCML, using the ``implements``
subdirective of the ``content`` or ``class`` directive.

Now let's create an annotation for this:

.. doctest::

   >>> from zope.component import adapts
   >>> from zope.interface import Attribute
   >>> class IBar(Interface):
   ...     a = Attribute('A')
   ...     b = Attribute('B')
   >>> from zope import component
   >>> @implementer(IBar)
   ... class Bar(object):
   ...     adapts(IFoo)
   ...     def __init__(self):
   ...         self.a = 1
   ...         self.b = 2

Note that the annotation implementation does not expect any arguments
to its ``__init__``. Otherwise it's basically an adapter.

Now, we'll register the annotation as an adapter. To do this we use
the :func:`~.factory` function provided by ``zope.annotation``:

.. doctest::

   >>> from zope.component import provideAdapter
   >>> from zope.annotation import factory
   >>> provideAdapter(factory(Bar))
   >>> from zope.component import provideAdapter
   >>> from zope.annotation.attribute import AttributeAnnotations
   >>> provideAdapter(AttributeAnnotations)

Note that we do not need to specify what the adapter provides or what
it adapts - we already do this on the annotation class itself.

Now let's make an instance of ``Foo``, and make an annotation for it.

.. doctest::

   >>> foo = Foo()
   >>> bar = IBar(foo)
   >>> bar.a
   1
   >>> bar.b
   2

We'll change ``a`` and get the annotation again. Our change is still
there:

.. doctest::

   >>> bar.a = 3
   >>> IBar(foo).a
   3

Of course it's still different for another instance of ``Foo``:

.. doctest::

   >>> foo2 = Foo()
   >>> IBar(foo2).a
   1

What if our annotation does not provide what it adapts with
``adapts``? It will complain:

.. doctest::

   >>> class IQux(Interface):
   ...     pass
   >>> @implementer(IQux)
   ... class Qux(object):
   ...     pass
   >>> provideAdapter(factory(Qux)) # doctest: +ELLIPSIS
   Traceback (most recent call last):
   ...
   TypeError: Missing 'zope.component.adapts' on annotation

It's possible to provide an annotation with an explicit key. (If the
key is not supplied, the key is deduced from the annotation's dotted
name, provided it is a class.)

.. doctest::

   >>> class IHoi(Interface):
   ...     pass
   >>> @implementer(IHoi)
   ... class Hoi(object):
   ...     adapts(IFoo)
   >>> provideAdapter(factory(Hoi, 'my.unique.key'))
   >>> isinstance(IHoi(foo), Hoi)
   True


Location
--------

Annotation factories are put into the location hierarchy with their parent
pointing to the annotated object and the name to the dotted name of the
annotation's class (or the name the adapter was registered under):

.. doctest::

   >>> foo3 = Foo()
   >>> new_hoi = IHoi(foo3)
   >>> new_hoi.__parent__
   <Foo object at 0x...>
   >>> new_hoi.__name__
   'my.unique.key'
   >>> import zope.location.interfaces
   >>> zope.location.interfaces.ILocation.providedBy(new_hoi)
   True

Please notice, that our Hoi object does not implement ILocation, so a
location proxy will be used. This has to be re-established every time we
retrieve the object

(Guard against former bug: proxy wasn't established when the annotation
existed already.)

.. doctest::

   >>> old_hoi = IHoi(foo3)
   >>> old_hoi.__parent__
   <Foo object at 0x...>
   >>> old_hoi.__name__
   'my.unique.key'
   >>> zope.location.interfaces.ILocation.providedBy(old_hoi)
   True


LocationProxies
---------------

Suppose your annotation proxy provides ILocation.

.. doctest::

   >>> class IPolloi(Interface):
   ...     pass
   >>> @implementer(IPolloi, zope.location.interfaces.ILocation)
   ... class Polloi(object):
   ...     adapts(IFoo)
   ...     __name__ = __parent__ = 0
   >>> provideAdapter(factory(Polloi, 'my.other.key'))

Sometimes you're adapting an object wrapped in a LocationProxy.

.. doctest::

   >>> foo4 = Foo()
   >>> import zope.location.location
   >>> wrapped_foo4 = zope.location.location.LocationProxy(foo4, None, 'foo4')
   >>> located_polloi = IPolloi(wrapped_foo4)

At first glance it looks as if located_polloi is located under wrapped_foo4.

.. doctest::

   >>> located_polloi.__parent__ is wrapped_foo4
   True
   >>> located_polloi.__name__
   'my.other.key'

but that's because we received a LocationProxy

.. doctest::

   >>> type(located_polloi).__name__
   'LocationProxy'

If we unwrap located_polloi and look at it directly, we'll see it stores a
reference to the real Foo object

.. doctest::

   >>> from zope.proxy import removeAllProxies
   >>> removeAllProxies(located_polloi).__parent__ == foo4
   True
   >>> removeAllProxies(located_polloi).__name__
   'my.other.key'

.. testcleanup::

   from zope.testing import cleanup
   cleanup.tearDown()
