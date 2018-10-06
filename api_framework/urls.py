from .settings import api_settings
from .utils.geturls import ServiceGetUrls

def api_urls():
    factory_def = api_settings.load_class(api_settings.MODULE_FACTORY)
    module_def = {k: api_settings.load_class(v) for k,v in api_settings.MODULES}
    api_def = {k: api_settings.load_class(v) for k,v in api_settings.APIS}

    modules = factory_def(module_def)

    return [
        ServiceGetUrls(api(modules), path)
        for api, path in api_def.items()
    ]
