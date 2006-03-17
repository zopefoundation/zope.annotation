import zope.component
import zope.interface
from zope.app.annotation.interfaces import IAnnotations
import zope.app.container.contained

def factory(factory, key=None):
    """Adapter factory to help create annotations easily.
    """
    # if no key is provided,
    # we'll determine the unique key based on the factory's dotted name
    if key is None:
        key = factory.__module__ + '.' + factory.__name__

    adapts = zope.component.adaptedBy(factory)
    if adapts is None:
        raise TypeError("Missing 'zope.component.adapts' on annotation")

    @zope.component.adapter(list(adapts)[0])
    @zope.interface.implementer(list(zope.component.implementedBy(factory))[0])
    def getAnnotation(context):
        annotations = IAnnotations(context)
        try:
            return annotations[key]
        except KeyError:
            result = factory()
            annotations[key] = result
            zope.app.container.contained.contained(
                result, context, key)
            return result

    # Convention to make adapter introspectable, used by apidoc
    getAnnotation.factory = factory 
    return getAnnotation
