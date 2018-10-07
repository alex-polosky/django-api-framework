import importlib
from django.conf import settings

NAME = 'API_FRAMEWORK'

DEFAULTS = {
    # 'DEFAULT_PERMISSION': '',
    # 'DEFAULT_RENDER': '',
    # 'DEFAULT_IN_LOOKUPTYPE': '',
    # 'DEFAULT_IN_CONVERTTYPE': '',
    # 'DEFAULT_IN_LOOKUP': '',
    # 'DEFAULT_OUT_CONVERTTYPE': '',
    'MODULE_FACTORY': 'api_framework.module.ModuleFactory',
    'MODULES': {},
    'APIS': {}
}

class Settings(object):

    def __init__(self, defaults=None, conf=None):
        self.defaults = defaults or DEFAULTS
        self.conf = conf or getattr(settings, NAME)

    def __getattr__(self, attr):
        if attr not in DEFAULTS:
            raise AttributeError('Invalid setting for "{}": "{}"'.format(NAME, attr))

        try:
            return self.conf[attr]
        except KeyError:
            return self.defaults[attr]

    def load_class(self, clsString):
        parts = clsString.split('.')
        module = importlib.import_module('.'.join(parts[:-1]))
        return getattr(module, parts[-1])

api_settings = Settings()
