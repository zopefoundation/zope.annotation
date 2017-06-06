Changes
=======

4.6 (unreleased)
----------------

- Optimize ``AttributeAnnotations`` for speed. In the case that only
  one method is called on a given instance, there should be no
  difference. But if more than one method is called, there should be a
  speed increase (such as the common pattern ``if 'key' not in
  annotations: annotations['key'] = value``). A consequence is that
  read-only operations on a given AttributeAnnotations instance will
  not immediately reflect changes made to other extant
  ``AttributeAnnotations`` objects, *if* the
  underlying object had no annotations to begin with. See `issue 8
  <https://github.com/zopefoundation/zope.annotation/issues/8>`_.


4.5 (2017-06-03)
----------------

- Drop support for Python 2.6.

- Claim support for Python 3.5 and 3.6.

- Reach 100% test coverage.

- ``AttributeAnnotations`` is now always a
  ``collections.MutableMapping``. Previously on Python 2 it was a
  ``UserDict.DictMixin``.

4.4.1 (2015-01-09)
------------------

- Convert doctests to Sphinx documentation.  Doctest snippets are still
  tested via ``tox -e docs``.


4.4.0 (2015-01-09)
------------------

- LP #98462:  add additional "iterable mapping" methods to ``IAnnotations``.

- LP #878265:

  - Make ``persistent`` (used only for doctests) a soft dependency,
    installable via the ``zope.annotation[btree]`` extra.

  - Make ``BTrees`` (used for attribute storage) a soft dependency,
    installable via the ``zope.annotation[btree]`` extra.  Fall back to
    using ``dict`` for attribute storage if ``BTrees`` is not importable.

4.3.0 (2014-12-26)
------------------

- Add support for Python 3.4.

4.2.0 (2013-03-18)
------------------

- Don't make AttributeAnnotations available as a view.

4.1.0 (2013-02-24)
------------------

- Add ``__bool__`` method to ``IAnnotations`` API for Python 3 compatibility.

4.0.1 (2013-02-11)
------------------

- Add `tox.ini`.

4.0.0 (2013-02-11)
------------------

- Add support for Python 3.3 and PyPy.

- Replace deprecated ``zope.component.adapts`` usage with equivalent
  ``zope.component.adapter`` decorator.

- Replace deprecated ``zope.interface.implements`` usage with equivalent
  ``zope.interface.implementer`` decorator.

- Drop support for Python 2.4 and 2.5.

- Include zcml dependencies in configure.zcml, require the necessary packages
  via a zcml extra, added tests for zcml.

3.5.0 (2009-09-07)
------------------

- Add ZODB3 to install_requires, because it's a true requirement of this
  package, not just a testing requirement, as BTrees are in use.

- Fix one test that was inactive because it's function was overriden by
  a mistake.

3.4.2 (2009-03-09)
------------------

- Clean up package description and documentation a bit.

- Change mailing list address to zope-dev at zope.org, as
  zope3-dev at zope.org is now retired.

- Remove old zpkg-related files.

3.4.1 (2008-08-26)
------------------

- Annotation factories take care not to store proxies in the database,
  so adapting an object wrapped in a ``LocationProxy`` works correctly.
  Fixes https://bugs.launchpad.net/zope3/+bug/261620

3.4.0 (2007-08-29)
------------------

- Annotation factories are no longer containing the factored object.
  Instead the objects are located using ``zope.location``. This removes
  a dependency to ``zope.app.container``.
