from ..definitions.inputparameter import InputParameterDefinition
from ..definitions.method import MethodDefinition
from .method import ServiceMethod

class ServiceInputParameter(object):
    
    def __call__(self, name, lookupType=str, convertType=None, convertLookup='id', optional=False, default=None):
        
        def decorator(func):
            if name:
                _name = name
            else:
                _name = func.__name__
            
            if not hasattr(func, ServiceMethod.PARAM):
                methodDefinition = MethodDefinition(func)
                setattr(func, ServiceMethod.PARAM, methodDefinition)
            else:
                methodDefinition = getattr(func, ServiceMethod.PARAM)
            
            parameter = InputParameterDefinition(name, lookupType, convertType, convertLookup, optional, default)
            methodDefinition.inputs.append(parameter)
            
            return func
        
        return decorator
    
    # The parameters are just for intellisense
    def __init__(self, name='', lookupType=str, convertType=None, convertLookup='id', optional=False, default=None):
        return
