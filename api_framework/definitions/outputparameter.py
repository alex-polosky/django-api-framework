class OutputParameterDefinition(object):

    @property
    def name(self):
        return self._name
    
    @property
    def optional(self):
        return self._optional
    
    @property
    def convertType(self):
        return self._convertType
    
    @property
    def many(self):
        return self._many
    
    @property
    def page(self):
        return self._page
    
    @property
    def per_page(self):
        return self._per_page
    
    def generate(self, request):
        pass
    
    def validate(self, request):
        return False
    
    def clone(self):
        op = OutputParameterDefinition(self.name, self.convertType, self.many, self.optional, self.page, self.per_page)
        return op
    
    def __init__(self, name, convertType=None, many=False, optional=False, page=False, per_page=None):
        self._name = name
        self._convertType = convertType
        self._many = many
        self._optional = optional
        self._page = page
        self._per_page = per_page
