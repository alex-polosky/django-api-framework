from .base import BaseModule

class ModuleFactory(object):

    @classmethod
    def instance(cls):
        if not hasattr(cls, '__SINGLETON'):
            setattr(cls, '__SINGLETON', cls())
        return getattr(cls, '__SINGLETON')

    def __init__(self, **kwargs):
        for name, cls in kwargs.items():
            if not issubclass(cls, BaseModule):
                raise TypeError('Cannot set module from class "{}" in factory as it does not derive from BaseModule'.format(cls))
            setattr(self, name, cls(self))
