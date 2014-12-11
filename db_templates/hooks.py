'''
Created on 11 dec 2014

@author: thomas
'''
import types
import collections

class HookRegistry(object):
    def __init__(self):
        self._hooks = {}
    
    """Register a method with hook name. Method must have this definition method(name, context, **kwargs) where name id the hook name.
    """
    def register(self, names, method):
        if not isinstance(names, collections.Iterable):
            names = [names]
        for name in names:
            if not name in self._hooks:
                self._hooks[name] = []
            self._hooks[name].append(method)
        
    def unregister(self, names, method):
        if not isinstance(names, collections.Iterable):
            names = [names]
        for name in names:
            self._hooks[name].remove(method)
    
    def get_methods(self, name):
        return self._hooks[name]
    
    def get_output(self, name, context, **kwargs):
        output = ""
        for method in registry.get_methods(name):
            output += method(name, context, **kwargs)
        return output
    
registry = HookRegistry()