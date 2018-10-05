from .collection import ServiceCollection
from .endpoint import ServiceEndpoint
from .getmethods import ServiceGetMethods
from .geturls import ServiceGetUrls
from .inputparameter import ServiceInputParameter
from .method import ServiceMethod
from .outputparameter import ServiceOutputParameter
from .response import ServiceResponse

ServiceEndpoint = ServiceEndpoint()
ServiceMethod = ServiceMethod()
ServiceInputParameter = ServiceInputParameter()
ServiceOutputParameter = ServiceOutputParameter()

__all__ = [
    'ServiceCollection',
    'ServiceEndpoint',
    'ServiceGetMethods',
    'ServiceGetUrls',
    'ServiceInputParameter',
    'ServiceMethod',
    'ServiceOutputParameter',
    'ServiceResponse'
]
