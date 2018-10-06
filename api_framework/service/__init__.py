from .collection import ServiceCollection
from .endpoint import ServiceEndpoint
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
    'ServiceInputParameter',
    'ServiceMethod',
    'ServiceOutputParameter',
    'ServiceResponse'
]
