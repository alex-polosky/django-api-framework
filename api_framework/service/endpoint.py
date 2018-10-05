from ..definitions.endpoint import EndpointDefinition
from .method import ServiceMethod

class ServiceEndpoint(object):

    PARAM = '__service_endpoint__'
    
    def getEndpoint(self, name):
        return self._endpoints[name]

    def getEndpoints(self):
        return self._endpoints

    def __call__(self, name=None):

        def decorator(clas):
            if name:
                _name = name
            else:
                _name = clas.__name__
            
            if hasattr(clas, ServiceEndpoint.PARAM):
                raise AttributeError("Class '{0}' is already defined as an endpoint".format(clas))
            if _name in self._endpoints:
                ep = ServiceEndpoint.endpoints[_name]
                raise AttributeError("Class '{0}' tried to define an endpoint for '{1}', which is already set by '{2}'".format(clas, _name, ep))
            
            methods = {}
            for varName, var in vars(clas).items():
                if varName[0] == '_':
                    continue
                if var.__class__.__name__ != 'function':
                    continue
                if not hasattr(var, ServiceMethod.PARAM):
                    continue
                
                methodDefinition = getattr(var, ServiceMethod.PARAM)
                if methodDefinition.name in methods:
                    raise AttributeError("Class '{0}' already contains an api call named '{1}' which is set by '{2}'".format(clas, methodDefinition.name, methodDefinition.func))
                
                methods[methodDefinition.name] = methodDefinition
            
            endpointDefinition = EndpointDefinition(clas, _name, methods)
            setattr(clas, ServiceEndpoint.PARAM, endpointDefinition)
            self._endpoints[_name] = endpointDefinition
            
            return clas
        
        return decorator

    # The parameters are just for intellisense
    def __init__(self, name=None):
        self._endpoints = {}
