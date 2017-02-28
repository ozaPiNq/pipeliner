from six import with_metaclass


class Singleton(type):
    _instance = None

    def __call__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = type.__call__(cls, *args, **kwargs)
        return cls._instance


class Register(with_metaclass(Singleton, object)):
    """
    Handles task registration (including providers control)
    """
    def add_handler(self, func_name, depends=[], provides=[]):
        pass
