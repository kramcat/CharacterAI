class pyCAIError(Exception):
    pass

class NoResponse(pyCAIError):
    pass

class CharNotFound(pyCAIError):
    pass