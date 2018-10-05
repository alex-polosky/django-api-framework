class NamedHashMap(object):
    def __init__(self):
        return

    def __setitem__(self, key, value):
        if type(key) == str and len(key) > 0 and key[0] == '_':
            self.__dict__[key] = value
            return

        if key in self.__dict__:
            del self.__dict__[self.__dict__[key]]
            del self.__dict__[key]
        elif value in self.__dict__:
            del self.__dict__[self.__dict__[value]]
            del self.__dict__[value]
        
        self.__dict__[key] = value
        self.__dict__[value] = key

    def __getitem__(self, key):
        if key in self.__dict__:
            return self.__dict__[key]
        return None

    def __setattr__(self, key, value):
        if type(key) == str and len(key) > 0 and key[0] == '_':
            self.__dict__[key] = value
            return

        if key in self.__dict__:
            del self.__dict__[self.__dict__[key]]
            del self.__dict__[key]
        elif value in self.__dict__:
            del self.__dict__[self.__dict__[value]]
            del self.__dict__[value]
        
        self.__dict__[key] = value
        self.__dict__[value] = key
