from enum import Enum
from functools import wraps
import json

from django.conf import settings
from django.conf.urls import url, include
import django.views.decorators.csrf as csrf

from rest_framework import authentication, decorators, permissions
from rest_framework.renderers import JSONRenderer, StaticHTMLRenderer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer

# class CsrfExemptSessionAuthentication(authentication.SessionAuthentication):

#     def enforce_csrf(self, request):
#         return  # To not perform the csrf check previously happening

# class NamedDict(object):
#     def __init__(self, dict={}):
#         self.__dict__.update(dict)

#     def __setitem__(self, key, value):
#         self.__dict__[key] = value

#     def __getitem__(self, key):
#         if key in self.__dict__:
#             return self.__dict__[key]
#         return None

#     def __setattr__(self, key, value):
#         self.__dict__[key] = value

# class NamedHashMap(object):
#     def __init__(self):
#         return

#     def __setitem__(self, key, value):
#         if type(key) == str and len(key) > 0 and key[0] == '_':
#             self.__dict__[key] = value
#             return

#         if key in self.__dict__:
#             del self.__dict__[self.__dict__[key]]
#             del self.__dict__[key]
#         elif value in self.__dict__:
#             del self.__dict__[self.__dict__[value]]
#             del self.__dict__[value]
        
#         self.__dict__[key] = value
#         self.__dict__[value] = key

#     def __getitem__(self, key):
#         if key in self.__dict__:
#             return self.__dict__[key]
#         return None

#     def __setattr__(self, key, value):
#         if type(key) == str and len(key) > 0 and key[0] == '_':
#             self.__dict__[key] = value
#             return

#         if key in self.__dict__:
#             del self.__dict__[self.__dict__[key]]
#             del self.__dict__[key]
#         elif value in self.__dict__:
#             del self.__dict__[self.__dict__[value]]
#             del self.__dict__[value]
        
#         self.__dict__[key] = value
#         self.__dict__[value] = key

# class ServiceCollection(object):

#     _modules = None

#     def __init__(self, moduleFactory):
#         self._modules = moduleFactory

# class ServiceException(BaseException):

#     class ERRORS:#(Enum):
#         SERVER_NOT_REACHABLE = -1
#         NONE = 0
#         UNKNOWN = 1
#         NO_CUSTOMER = 2
#         INVALID_ID = 3
#         REQUIRED = 4
#         BAD_CONVERT = 5
#         DB_NOT_FOUND = 6
#         INVALID = 7
#         ALREADY_EXISTS = 8
#         INACTIVE = 9
#         HAS_TAB = 10
#         CLOCKED_IN = 11
#         NO_PAYMENT = 12
#         BAD_PAYMENT = 13
#         PROCESSING = 14
#         QUERY_LIMIT = 15
    
#     @property
#     def additional(self):
#         return self._additional

#     @property
#     def displayToUser(self):
#         return self._displayToUser

#     @property
#     def errorCode(self):
#         return self._errorCode
    
#     @property
#     def message(self):
#         return self._message
    
#     @property
#     def responseCode(self):
#         return self._responseCode
    
#     def toResponseObject(self):
#         toret = {'message': self.message}
#         toret.update(self.additional)
#         return toret
    
#     def __init__(self, message=None, errorCode=0, displayToUser=False, responseCode=400, additional=None):
#         if message:
#             super().__init__(message)
#         else:
#             super().__init__()
        
#         self._message = message
#         self._errorCode = errorCode
#         self._displayToUser = displayToUser
#         self._responseCode = responseCode
#         self._additional = additional or { }

# class EndpointDefinition(object):

#     @property
#     def clas(self):
#         return self._clas

#     @property
#     def name(self):
#         return self._name
    
#     @property
#     def methods(self):
#         return self._methods

#     def __init__(self, clas, name, methods=None):
#         if not methods:
#             methods = {}
#         self._clas = clas
#         self._name = name
#         self._methods = methods

# class MethodDefinition(object):

#     @property
#     def func(self):
#         return self._func

#     @property
#     def inputs(self):
#         return self._inputs

#     @property
#     def name(self):
#         return self._name

#     @property
#     def outputs(self):
#         return self._outputs
    
#     @property
#     def methods(self):
#         return self._methods
    
#     @property
#     def permission(self):
#         return self._permissions
    
#     @property
#     def serviceMethod(self):
#         return self._serviceMethod
    
#     @property
#     def wrapperFunc(self):
#         return self._wrappedFunc
    
#     def clone(self):
#         md = MethodDefinition(self.func, self.serviceMethod, self.name, self.permission, self.methods)
#         md._wrapperFunc = self.wrapperFunc
#         for ip in self.inputs:
#             md.inputs.append(ip.clone())
#         for op in self.outputs:
#             md.outputs.append(op.clone())
#         return md
    
#     def __init__(self, func=None, serviceMethod=None, name=None, permissions=None, methods=None):
#         self._func = func
#         self._serviceMethod = serviceMethod
#         self._name = name
#         self._permissions = permissions
#         self._methods = methods
#         self._inputs = []
#         self._outputs = []

# class InputParameterDefinition(object):

#     @property
#     def name(self):
#         return self._name
    
#     @property
#     def lookupType(self):
#         return self._lookupType

#     @property
#     def convertType(self):
#         return self._convertType
    
#     @property
#     def convertLookup(self):
#         return self._convertLookup
    
#     @property
#     def optional(self):
#         return self._optional
    
#     @property
#     def default(self):
#         return self._default
    
#     def generate(self, request):
#         parameter = None

#         value = request.data.get(self.name, None)
#         if value != None:
#             if type(value) == tuple or type(value) == list:
#                 values = value
#             else:
#                 if value == "":
#                     values = None
#                 else:
#                     values = [value]
#         else:
#             values = None

#         if values and len(values) > 0:
#             parameter = []
#             for value in values:
#                 try:

#                     lookup = self.lookupType(value)
#                 except (TypeError, ValueError):
#                     raise ServiceException("Could not convert parameter to lookup type: {0}".format(name), ServiceException.ERRORS.BAD_CONVERT, additional={'inputParamater': self.name})

#                 if self.convertType:
#                     try:
#                         params = { self.convertLookup: lookup }
#                         convert = self.convertType.objects.get(**params)
#                     except self.convertType.DoesNotExist as ex:
#                         raise ServiceException(ex.message, ServiceException.DB_NOT_FOUND)
#                 else:
#                     convert = lookup
#                 parameter.append(convert)

#             if len(parameter) == 1:
#                 parameter = parameter[0]

#         else:
#             if self.optional or self.default != None:
#                 parameter = self.default
#             else:
#                 raise ServiceException("Parameter required but not found: {0}".format(self.name), ServiceException.ERRORS.REQUIRED, additional={'inputParamater': self.name})
        
#         return parameter
    
#     def clone(self):
#         ip = InputParameterDefinition(self.name, self.lookupType, self.convertType, self.convertLookup, self.optional, self.default)
#         return ip

#     def __init__(self, name, lookupType=str, convertType=None, convertLookup='id', optional=False, default=None):
#         self._name = name
#         self._lookupType = lookupType
#         self._convertType = convertType
#         self._convertLookup = convertLookup
#         self._optional = optional
#         self._default = default
#         if self._default:
#             self._optional = True

# class OutputParameterDefinition(object):

#     @property
#     def name(self):
#         return self._name
    
#     @property
#     def optional(self):
#         return self._optional
    
#     @property
#     def convertType(self):
#         return self._convertType
    
#     @property
#     def many(self):
#         return self._many
    
#     @property
#     def page(self):
#         return self._page
    
#     @property
#     def per_page(self):
#         return self._per_page
    
#     def generate(self, request):
#         pass
    
#     def validate(self, request):
#         return False
    
#     def clone(self):
#         op = OutputParameterDefinition(self.name, self.convertType, self.many, self.optional, self.page, self.per_page)
#         return op
    
#     def __init__(self, name, convertType=None, many=False, optional=False, page=False, per_page=None):
#         self._name = name
#         self._convertType = convertType
#         self._many = many
#         self._optional = optional
#         self._page = page
#         self._per_page = per_page

# class ServiceEndpoint(object):

#     PARAM = '__service_endpoint__'
    
#     def getEndpoint(self, name):
#         return self._endpoints[name]

#     def getEndpoints(self):
#         return self._endpoints

#     def __call__(self, name=None):

#         def decorator(clas):
#             if name:
#                 _name = name
#             else:
#                 _name = clas.__name__
            
#             if hasattr(clas, ServiceEndpoint.PARAM):
#                 raise AttributeError("Class '{0}' is already defined as an endpoint".format(clas))
#             if _name in self._endpoints:
#                 ep = ServiceEndpoint.endpoints[_name]
#                 raise AttributeError("Class '{0}' tried to define an endpoint for '{1}', which is already set by '{2}'".format(clas, _name, ep))
            
#             methods = {}
#             for varName, var in vars(clas).items():
#                 if varName[0] == '_':
#                     continue
#                 if var.__class__.__name__ != 'function':
#                     continue
#                 if not hasattr(var, ServiceMethod.PARAM):
#                     continue
                
#                 methodDefinition = getattr(var, ServiceMethod.PARAM)
#                 if methodDefinition.name in methods:
#                     raise AttributeError("Class '{0}' already contains an api call named '{1}' which is set by '{2}'".format(clas, methodDefinition.name, methodDefinition.func))
                
#                 methods[methodDefinition.name] = methodDefinition
            
#             endpointDefinition = EndpointDefinition(clas, _name, methods)
#             setattr(clas, ServiceEndpoint.PARAM, endpointDefinition)
#             self._endpoints[_name] = endpointDefinition
            
#             return clas
        
#         return decorator

#     # The parameters are just for intellisense
#     def __init__(self, name=None):
#         self._endpoints = {}

# class ServiceMethod(object):

#     PARAM = '__service_method__'

#     def __call__(self, name=None, permissions=(permissions.IsAuthenticated,), methods=('POST',)):

#         def decorator(func):
#             if name:
#                 _name = name
#             else:
#                 _name = func.__name__
            
#             if not hasattr(func, ServiceMethod.PARAM):
#                 methodDefinition = MethodDefinition(func, None, _name, permissions, methods)
#                 setattr(func, ServiceMethod.PARAM, methodDefinition)
#             else:
#                 methodDefinition = getattr(func, ServiceMethod.PARAM)
#                 methodDefinition._name = _name
#                 methodDefinition._permissions = permissions
#                 methodDefinition._methods = methods

#             @wraps(func)
#             def execute_request(request, modules=None):
#                 methodDefinition = getattr(func, ServiceMethod.PARAM)

#                 request.inputs = NamedDict()
#                 request.outputs = NamedDict()

#                 user = request.user
#                 tokenObj = request.auth
#                 if user and tokenObj:
#                     request.inputs.user = user
#                     request.inputs.token = tokenObj.key
#                     request.inputs.tokenObject = tokenObj
                
#                 for inputParamter in methodDefinition.inputs:
#                     try:
#                         request.inputs[inputParamter.name] = inputParamter.generate(request)
#                     except ServiceException as ex:
#                         # TODO: implement logging
#                         if settings.DEBUG:
#                             return ServiceResponse(request, ex.responseCode, ex.errorCode, ex.toResponseObject())
#                         else:
#                             if ex.displayToUser:
#                                 return ServiceResponse(request, ex.responseCode, ex.errorCode, ex.toResponseObject())
#                             else:
#                                 return ServiceResponse(request, ex.responseCode, ServiceException.ERRORS.INVALID_ID)
#                     except BaseException as ex:
#                         if settings.DEBUG:
#                             return ServiceResponse(request, 500, ServiceException.ERRORS.UNKNOWN, {
#                                 'inputParameter': inputParamter.name,
#                                 'message': str(ex),
#                                 'type': ex.__class__.__name__
#                             })
#                         else:
#                             return ServiceResponse(request, 500, ServiceException.ERRORS.UNKNOWN)
                
#                 try:
#                     if modules:
#                         func(request, modules)
#                     else:
#                         func(request)
#                 except ServiceException as ex:
#                     if settings.DEBUG:
#                         return ServiceResponse(request, ex.responseCode, ex.errorCode, ex.toResponseObject())
#                     if ex.displayToUser:
#                         return ServiceResponse(request, ex.responseCode, ex.errorCode, ex.additional)
#                     return ServiceResponse(request, 400, ServiceException.ERRORS.UNKNOWN)
#                 except BaseException as ex:
#                     if settings.DEBUG:
#                         import traceback
#                         return ServiceResponse(request, 500, ServiceException.ERRORS.UNKNOWN, {
#                             'message': str(ex),
#                             'type': ex.__class__.__name__,
#                             'stack': traceback.format_exc()
#                         })
#                     else:
#                         return ServiceResponse(request, 500, ServiceException.ERRORS.UNKNOWN)

#                 context = {'request': request}
#                 for outputParameter in methodDefinition.outputs:
#                     if hasattr(request.outputs, outputParameter.name):
#                         param = getattr(request.outputs, outputParameter.name)
#                         param_out = None
#                         convert = outputParameter.convertType

#                         if convert and issubclass(convert, BaseSerializer):
#                             serialized = convert(param, context=context, many=outputParameter.many)
#                             param_out = serialized.data
#                         elif convert and issubclass(convert, dict):
#                             pass
#                         elif convert != None and callable(convert):
#                             param_out = convert(param)
#                         else:
#                             param_out = param
#                             #param_out = json.dumps(param)
                        
#                         setattr(request.outputs, outputParameter.name, param_out)
                    
#                     elif not outputParameter.optional:
#                         pass # Throw error here?

#                 return ServiceResponse(request, 200)
            
#             methodDefinition._wrappedFunc = execute_request

#             wrapper = decorators.authentication_classes((authentication.TokenAuthentication,CsrfExemptSessionAuthentication))(execute_request)
#             wrapper = decorators.permission_classes(permissions)(wrapper)
#             wrapper = decorators.renderer_classes((JSONRenderer,))(wrapper)
#             wrapper = decorators.api_view(methods)(wrapper)

#             @wraps(wrapper)
#             def ensure_arguments(*args):
#                 if len(args) == 1:
#                     request = args[0]
#                     modules = None
#                 elif len(args) == 2:
#                     request = args[1]
#                     cls_instance = args[0]
#                     modules = cls_instance._modules

#                 return wrapper(request, modules)
            
#             methodDefinition._serviceMethod = ensure_arguments
#             setattr(ensure_arguments, ServiceMethod.PARAM, methodDefinition)
            
#             return ensure_arguments
        
#         return decorator

#     # The parameters are just for intellisense
#     def __init__(self, name=None, permissions=(permissions.IsAuthenticated,), methods=('POST',)):
#         return

# class ServiceInputParameter(object):
    
#     def __call__(self, name, lookupType=str, convertType=None, convertLookup='id', optional=False, default=None):
        
#         def decorator(func):
#             if name:
#                 _name = name
#             else:
#                 _name = func.__name__
            
#             if not hasattr(func, ServiceMethod.PARAM):
#                 methodDefinition = MethodDefinition(func)
#                 setattr(func, ServiceMethod.PARAM, methodDefinition)
#             else:
#                 methodDefinition = getattr(func, ServiceMethod.PARAM)
            
#             parameter = InputParameterDefinition(name, lookupType, convertType, convertLookup, optional, default)
#             methodDefinition.inputs.append(parameter)
            
#             return func
        
#         return decorator
    
#     # The parameters are just for intellisense
#     def __init__(self, name='', lookupType=str, convertType=None, convertLookup='id', optional=False, default=None):
#         return

# class ServiceOutputParameter(object):
    
#     def __call__(self, name, convertType=None, many=False, optional=False, page=False, per_page=None):

#         def decorator(func):
#             if name:
#                 _name = name
#             else:
#                 _name = func.__name__
            
#             if not hasattr(func, ServiceMethod.PARAM):
#                 methodDefinition = MethodDefinition(func)
#                 setattr(func, ServiceMethod.PARAM, methodDefinition)
#             else:
#                 methodDefinition = getattr(func, ServiceMethod.PARAM)
            
#             parameter = OutputParameterDefinition(name, convertType, many, optional, page, per_page)
#             methodDefinition.outputs.append(parameter)

#             return func
        
#         return decorator
    
#     # The parameters are just for intellisense
#     def __init__(self, name='', convertType=None, many=False, optional=False, page=False, per_page=None):
#         return

# def ServiceResponse(request, responseCode, errorCode=None, errorAdditional=None):
#     response = { }

#     if responseCode != 200:
#         if not errorCode:
#             errorCode = ServiceException.ERRORS.UNKNOWN
#         if not errorAdditional:
#             errorAdditional = {}
#         response = {'status': errorCode, 'add': errorAdditional}
    
#     response.update(request.outputs.__dict__)

#     return Response(response, responseCode)

# def ServiceGetMethods(class_instance):
#     if class_instance.__class__ == type:
#         #raise NotImplementedError()
#         items = vars(class_instance).items()
#     else:
#         items = dir(class_instance)
    
#     methods = {}

#     for varName in items:
#         try:
#             var = getattr(class_instance, varName)
#             if varName[0] == '_':
#                 continue
#             if var.__class__.__name__ != 'function' and var.__class__.__name__ != 'method':
#                 continue
#             methodDefinition = getattr(var, ServiceMethod.PARAM, None)
#             serviceMethod = var
#         except TypeError as ex:
#             methodDefinition = getattr(varName[1], ServiceMethod.PARAM, None)
#             serviceMethod = varName

#         #methodDefinition = getattr(var, ServiceMethod.PARAM, None)
#         if methodDefinition:
#             if methodDefinition.name in methods:
#                 raise AttributeError("Class '{0}' already contains an api call named '{1}' which is set by '{2}'".format(cls, methodDefinition.name, methodDefinition.func))
            
#             methods[methodDefinition.name] = methodDefinition.clone()
#             methods[methodDefinition.name]._serviceMethod = serviceMethod
#             setattr(methods[methodDefinition.name], ServiceMethod.PARAM, methodDefinition)
    
#     return list(methods.values())

# def ServiceGetUrls(class_instance, endpoint):
#     urls = []
#     for method in ServiceGetMethods(class_instance):
#         urls.append(url(method.name + '/', method.serviceMethod))
    
#     return url('^' + endpoint + '/', include(urls))

ServiceEndpoint = ServiceEndpoint()
ServiceMethod = ServiceMethod()
ServiceInputParameter = ServiceInputParameter()
ServiceOutputParameter = ServiceOutputParameter()
