class ServiceCollection(object):

    _modules = None
    
    def __init__(self, moduleFactory):
        self._modules = moduleFactory
