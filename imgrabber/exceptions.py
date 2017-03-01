class RegisterException(Exception):
    pass


class TaskAlreadyRegistered(RegisterException):
    pass


class TaskNotFound(RegisterException):
    pass
