from .method import ServiceMethod

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
            methodDefinition = getattr(var, ServiceMethod.PARAM, None)
            serviceMethod = var
        except TypeError as ex:
            methodDefinition = getattr(varName[1], ServiceMethod.PARAM, None)
            serviceMethod = varName

        #methodDefinition = getattr(var, ServiceMethod.PARAM, None)
        if methodDefinition:
            if methodDefinition.name in methods:
                raise AttributeError("Class '{0}' already contains an api call named '{1}' which is set by '{2}'".format(cls, methodDefinition.name, methodDefinition.func))
            
            methods[methodDefinition.name] = methodDefinition.clone()
            methods[methodDefinition.name]._serviceMethod = serviceMethod
            setattr(methods[methodDefinition.name], ServiceMethod.PARAM, methodDefinition)
    
    return list(methods.values())
