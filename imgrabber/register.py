from six import with_metaclass
from imgrabber.exceptions import TaskAlreadyRegistered, TaskNotFound


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

    _handlers = {}

    def add_handler(self, func_name, depends=[], provides=[]):
        if func_name not in self._handlers:
            self._handlers[func_name] = dict(depends=depends, provides=provides)
        else:
            raise TaskAlreadyRegistered()

    def get_handler(self, func_name):
        if func_name in self._handlers:
            return self._handlers[func_name]
        else:
            raise TaskNotFound()

    def _clear(self):
        """ Remove all handlers """
        self._handlers = {}
