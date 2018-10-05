from rest_framework.response import Response

from ..exceptions import ServiceException

def ServiceResponse(request, responseCode, errorCode=None, errorAdditional=None):
    response = { }

    if responseCode != 200:
        if not errorCode:
            errorCode = ServiceException.ERRORS.UNKNOWN
        if not errorAdditional:
            errorAdditional = {}
        response = {'status': errorCode, 'add': errorAdditional}
    
    response.update(request.outputs.__dict__)

    return Response(response, responseCode)
