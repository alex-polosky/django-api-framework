from django.conf.urls import url as _url
from django.conf.urls import include as _include

from .service import ServiceMethod as _ServiceMethod
from .settings import api_settings as _api_settings

def ServiceGetMethods(class_instance):
    if class_instance.__class__ == type:
        #raise NotImplementedError()
        items = vars(class_instance).items()
    else:
        items = dir(class_instance)
    
    methods = {}

    for varName in items:
        try:
            var = getattr(class_instance, varName)
            if varName[0] == '_':
                continue
            if var.__class__.__name__ != 'function' and var.__class__.__name__ != 'method':
                continue
            methodDefinition = getattr(var, _ServiceMethod.PARAM, None)
            serviceMethod = var
        except TypeError as ex:
            methodDefinition = getattr(varName[1], ServiceMethod.PARAM, None)
            serviceMethod = varName

        if methodDefinition:
            if methodDefinition.name in methods:
                raise AttributeError("Class '{0}' already contains an api call named '{1}' which is set by '{2}'".format(cls, methodDefinition.name, methodDefinition.func))
            
            methods[methodDefinition.name] = methodDefinition.clone()
            methods[methodDefinition.name]._serviceMethod = serviceMethod
            setattr(methods[methodDefinition.name], ServiceMethod.PARAM, methodDefinition)
    
    return list(methods.values())

def ServiceGetUrls(class_instance, endpoint):
    urls = []
    for method in ServiceGetMethods(class_instance):
        urls.append(_url(method.name + '/', method.serviceMethod))
    return _url('^' + endpoint + '/', _include(urls))

def api_urls():
    factory_def = _api_settings.load_class(_api_settings.MODULE_FACTORY)
    module_def = {k: _api_settings.load_class(v) for k,v in _api_settings.MODULES.items()}
    api_def = {k: _api_settings.load_class(v) for k,v in _api_settings.APIS.items()}

    modules = factory_def(**module_def)

    return [
        ServiceGetUrls(api(modules), path)
        for path, api in api_def.items()
    ]
