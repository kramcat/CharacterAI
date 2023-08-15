class PyCAIError(Exception):
    pass

class ServerError(PyCAIError):
    pass

class FilterError(PyCAIError):
    pass

class NoChunksError(PyCAIError):
    pass

class NotFoundError(PyCAIError):
    pass

class LabelError(PyCAIError):
    pass

class AuthError(PyCAIError):
    pass

class NoResponse(PyCAIError):
    pass

class UnknownError(PyCAIError):
    pass

class PostTypeError(PyCAIError):
    pass