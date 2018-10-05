from ..definitions.method import MethodDefinition
from ..definitions.outputparameter import OutputParameterDefinition
from .method import ServiceMethod

class ServiceOutputParameter(object):
    
    def __call__(self, name, convertType=None, many=False, optional=False, page=False, per_page=None):

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
            
            parameter = OutputParameterDefinition(name, convertType, many, optional, page, per_page)
            methodDefinition.outputs.append(parameter)

            return func
        
        return decorator
    
    # The parameters are just for intellisense
    def __init__(self, name='', convertType=None, many=False, optional=False, page=False, per_page=None):
        return
