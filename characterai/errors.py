class PyCAIError(Exception):
    pass

class ServerError(PyCAIError):
    pass

class LabelError(PyCAIError):
    pass

class AuthError(PyCAIError):
    pass

class PostTypeError(PyCAIError):
    pass
