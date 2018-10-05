from ..exceptions import ServiceException

class InputParameterDefinition(object):

    @property
    def name(self):
        return self._name
    
    @property
    def lookupType(self):
        return self._lookupType

    @property
    def convertType(self):
        return self._convertType
    
    @property
    def convertLookup(self):
        return self._convertLookup
    
    @property
    def optional(self):
        return self._optional
    
    @property
    def default(self):
        return self._default
    
    def generate(self, request):
        parameter = None

        value = request.data.get(self.name, None)
        if value != None:
            if type(value) == tuple or type(value) == list:
                values = value
            else:
                if value == "":
                    values = None
                else:
                    values = [value]
        else:
            values = None

        if values and len(values) > 0:
            parameter = []
            for value in values:
                try:

                    lookup = self.lookupType(value)
                except (TypeError, ValueError):
                    raise ServiceException("Could not convert parameter to lookup type: {0}".format(name), ServiceException.ERRORS.BAD_CONVERT, additional={'inputParamater': self.name})

                if self.convertType:
                    try:
                        params = { self.convertLookup: lookup }
                        convert = self.convertType.objects.get(**params)
                    except self.convertType.DoesNotExist as ex:
                        raise ServiceException(ex.message, ServiceException.DB_NOT_FOUND)
                else:
                    convert = lookup
                parameter.append(convert)

            if len(parameter) == 1:
                parameter = parameter[0]

        else:
            if self.optional or self.default != None:
                parameter = self.default
            else:
                raise ServiceException("Parameter required but not found: {0}".format(self.name), ServiceException.ERRORS.REQUIRED, additional={'inputParamater': self.name})
        
        return parameter
    
    def clone(self):
        ip = InputParameterDefinition(self.name, self.lookupType, self.convertType, self.convertLookup, self.optional, self.default)
        return ip

    def __init__(self, name, lookupType=str, convertType=None, convertLookup='id', optional=False, default=None):
        self._name = name
        self._lookupType = lookupType
        self._convertType = convertType
        self._convertLookup = convertLookup
        self._optional = optional
        self._default = default
        if self._default:
            self._optional = True
