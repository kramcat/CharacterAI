class PyCAIError(Exception):
    pass

class ServerError(PyCAIError):
    pass

class FilterError(PyCAIError):
    pass

class NotFoundError(PyCAIError):
    pass

class LabelError(PyCAIError):
    pass

class AuthError(PyCAIError):
    pass

class WaitingRoom(PyCAIError):
    pass
