from odict import odict
from plumber import (
    plumb,
    extend,
    default,
    Part,
)
from zope.interface import implements
from node.interfaces import (
    INode,
    INodespaces,
)

class Nodespaces(Part):
    implements(INodespaces)
    
    _nodespaces = default(None)
    
    @extend
    @property
    def nodespaces(self):
        """A storage and general way to access our nodespaces.
        
        An ``AttributedNode`` uses this to store the ``attrs`` nodespace i.e.
        """
        if self._nodespaces is None:
            self._nodespaces = odict()
            self._nodespaces['__children__'] = self
        return self._nodespaces
    
    @plumb
    def __getitem__(prt, _next, self, key):
        # blend in our nodespaces as children, with name __<name>__
        # isinstance check is required because odict tries to get item possibly
        # with ``_nil`` key, which is actually an object
        if isinstance(key, basestring) \
          and key.startswith('__') \
          and key.endswith('__'):
            # a reserved child key mapped to the nodespace behind
            # nodespaces[key], nodespaces is an odict
            return self.nodespaces[key]
        return _next(self, key)
    
    @plumb
    def __setitem__(prt, _next, self, key, val):
        # blend in our nodespaces as children, with name __<name>__
        if key.startswith('__') and key.endswith('__'):
            # a reserved child key mapped to the nodespace behind
            # nodespaces[key], nodespaces is an odict
            val.__name__ = key
            val.__parent__ = self
            self.nodespaces[key] = val
            # index checks below must not happen for other nodespace.
            return
        _next(self, key, val)
    
    @plumb
    def __delitem__(prt, _next, self, key):
        # blend in our nodespaces as children, with name __<name>__
        if key.startswith('__') and key.endswith('__'):
            # a reserved child key mapped to the nodespace behind
            # nodespaces[key], nodespaces is an odict
            del self.nodespaces[key]
            return
        _next(self, key)