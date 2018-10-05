class NamedDict(object):
    def __init__(self, dict={}):
        self.__dict__.update(dict)

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def __getitem__(self, key):
        if key in self.__dict__:
            return self.__dict__[key]
        return None

    def __setattr__(self, key, value):
        self.__dict__[key] = value
