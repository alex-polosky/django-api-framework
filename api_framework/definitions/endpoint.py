class EndpointDefinition(object):

    @property
    def clas(self):
        return self._clas

    @property
    def name(self):
        return self._name
    
    @property
    def methods(self):
        return self._methods

    def __init__(self, clas, name, methods=None):
        if not methods:
            methods = {}
        self._clas = clas
        self._name = name
        self._methods = methods
