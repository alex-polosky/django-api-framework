class MethodDefinition(object):

    @property
    def func(self):
        return self._func

    @property
    def inputs(self):
        return self._inputs

    @property
    def name(self):
        return self._name

    @property
    def outputs(self):
        return self._outputs
    
    @property
    def methods(self):
        return self._methods
    
    @property
    def permission(self):
        return self._permissions
    
    @property
    def serviceMethod(self):
        return self._serviceMethod
    
    @property
    def wrapperFunc(self):
        return self._wrappedFunc
    
    def clone(self):
        md = MethodDefinition(self.func, self.serviceMethod, self.name, self.permission, self.methods)
        md._wrapperFunc = self.wrapperFunc
        for ip in self.inputs:
            md.inputs.append(ip.clone())
        for op in self.outputs:
            md.outputs.append(op.clone())
        return md
    
    def __init__(self, func=None, serviceMethod=None, name=None, permissions=None, methods=None):
        self._func = func
        self._serviceMethod = serviceMethod
        self._name = name
        self._permissions = permissions
        self._methods = methods
        self._inputs = []
        self._outputs = []
