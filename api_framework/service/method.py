from functools import wraps

from django.conf import settings

from .. import authentication
from .. import decorators
from .. import permissions
from .. import renderers
from ..definitions import MethodDefinition
from ..exceptions import ServiceException
from ..serializers import BaseSerializer
from ..utils import NamedDict

from .response import ServiceResponse

class ServiceMethod(object):

    PARAM = '__service_method__'

    def __call__(self, name=None, permissions=(permissions.IsAuthenticated,), methods=('POST',)):

        def decorator(func):
            if name:
                _name = name
            else:
                _name = func.__name__
            
            if not hasattr(func, ServiceMethod.PARAM):
                methodDefinition = MethodDefinition(func, None, _name, permissions, methods)
                setattr(func, ServiceMethod.PARAM, methodDefinition)
            else:
                methodDefinition = getattr(func, ServiceMethod.PARAM)
                methodDefinition._name = _name
                methodDefinition._permissions = permissions
                methodDefinition._methods = methods

            @wraps(func)
            def execute_request(request, modules=None):
                methodDefinition = getattr(func, ServiceMethod.PARAM)

                request.inputs = NamedDict()
                request.outputs = NamedDict()

                user = request.user
                tokenObj = request.auth
                if user and tokenObj:
                    request.inputs.user = user
                    request.inputs.token = tokenObj.key
                    request.inputs.tokenObject = tokenObj
                
                for inputParamter in methodDefinition.inputs:
                    try:
                        request.inputs[inputParamter.name] = inputParamter.generate(request)
                    except ServiceException as ex:
                        # TODO: implement logging
                        if settings.DEBUG:
                            return ServiceResponse(request, ex.responseCode, ex.errorCode, ex.toResponseObject())
                        else:
                            if ex.displayToUser:
                                return ServiceResponse(request, ex.responseCode, ex.errorCode, ex.toResponseObject())
                            else:
                                return ServiceResponse(request, ex.responseCode, ServiceException.ERRORS.INVALID_ID)
                    except BaseException as ex:
                        if settings.DEBUG:
                            return ServiceResponse(request, 500, ServiceException.ERRORS.UNKNOWN, {
                                'inputParameter': inputParamter.name,
                                'message': str(ex),
                                'type': ex.__class__.__name__
                            })
                        else:
                            return ServiceResponse(request, 500, ServiceException.ERRORS.UNKNOWN)
                
                try:
                    if modules:
                        func(request, modules)
                    else:
                        func(request)
                except ServiceException as ex:
                    if settings.DEBUG:
                        return ServiceResponse(request, ex.responseCode, ex.errorCode, ex.toResponseObject())
                    if ex.displayToUser:
                        return ServiceResponse(request, ex.responseCode, ex.errorCode, ex.additional)
                    return ServiceResponse(request, 400, ServiceException.ERRORS.UNKNOWN)
                except BaseException as ex:
                    if settings.DEBUG:
                        import traceback
                        return ServiceResponse(request, 500, ServiceException.ERRORS.UNKNOWN, {
                            'message': str(ex),
                            'type': ex.__class__.__name__,
                            'stack': traceback.format_exc()
                        })
                    else:
                        return ServiceResponse(request, 500, ServiceException.ERRORS.UNKNOWN)

                context = {'request': request}
                for outputParameter in methodDefinition.outputs:
                    if hasattr(request.outputs, outputParameter.name):
                        param = getattr(request.outputs, outputParameter.name)
                        param_out = None
                        convert = outputParameter.convertType

                        if convert and issubclass(convert, BaseSerializer):
                            serialized = convert(param, context=context, many=outputParameter.many)
                            param_out = serialized.data
                        elif convert and issubclass(convert, dict):
                            pass
                        elif convert != None and callable(convert):
                            param_out = convert(param)
                        else:
                            param_out = param
                            #param_out = json.dumps(param)
                        
                        setattr(request.outputs, outputParameter.name, param_out)
                    
                    elif not outputParameter.optional:
                        pass # Throw error here?

                return ServiceResponse(request, 200)
            
            methodDefinition._wrappedFunc = execute_request

            wrapper = decorators.authentication_classes((authentication.TokenAuthentication, authentication.CsrfExemptSessionAuthentication))(execute_request)
            wrapper = decorators.permission_classes(permissions)(wrapper)
            wrapper = decorators.renderer_classes((renderers.JSONRenderer,))(wrapper)
            wrapper = decorators.api_view(methods)(wrapper)

            @wraps(wrapper)
            def ensure_arguments(*args):
                if len(args) == 1:
                    request = args[0]
                    modules = None
                elif len(args) == 2:
                    request = args[1]
                    cls_instance = args[0]
                    modules = cls_instance._modules

                return wrapper(request, modules)
            
            methodDefinition._serviceMethod = ensure_arguments
            setattr(ensure_arguments, ServiceMethod.PARAM, methodDefinition)
            
            return ensure_arguments
        
        return decorator

    # The parameters are just for intellisense
    def __init__(self, name=None, permissions=(permissions.IsAuthenticated,), methods=('POST',)):
        return
