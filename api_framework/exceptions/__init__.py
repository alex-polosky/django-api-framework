# from enum import Enum

class ServiceException(BaseException):

    class ERRORS:  # (Enum):
        SERVER_NOT_REACHABLE = -1
        NONE = 0
        UNKNOWN = 1
        NO_CUSTOMER = 2
        INVALID_ID = 3
        REQUIRED = 4
        BAD_CONVERT = 5
        DB_NOT_FOUND = 6
        INVALID = 7
        ALREADY_EXISTS = 8
        INACTIVE = 9
        HAS_TAB = 10
        CLOCKED_IN = 11
        NO_PAYMENT = 12
        BAD_PAYMENT = 13
        PROCESSING = 14
        QUERY_LIMIT = 15
    
    @property
    def additional(self):
        return self._additional

    @property
    def displayToUser(self):
        return self._displayToUser

    @property
    def errorCode(self):
        return self._errorCode

    @property
    def message(self):
        return self._message

    @property
    def responseCode(self):
        return self._responseCode

    def toResponseObject(self):
        toret = {'message': self.message}
        toret.update(self.additional)
        return toret

    def __init__(self, message=None, errorCode=0, displayToUser=False, responseCode=400, additional=None):
        if message:
            super().__init__(message)
        else:
            super().__init__()

        self._message = message
        self._errorCode = errorCode
        self._displayToUser = displayToUser
        self._responseCode = responseCode
        self._additional = additional or { }
