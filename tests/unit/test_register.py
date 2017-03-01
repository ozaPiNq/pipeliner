import pytest

from imgrabber.register import Register
from imgrabber.exceptions import TaskAlreadyRegistered


def test_register_must_be_singleton():
    r1 = Register()
    r2 = Register()
    r3 = Register()

    assert id(r1) == id(r2) == id(r3)


class TestTaskHandling(object):
    def test_task_addition(self, register):
        def func():
            pass

        register.add_handler(func.__name__, depends=['d1', 'd2', 'd3'],
                             provides=['p1', 'p2'])

        register._handlers[func.__name__] = dict(depends=['d1', 'd2', 'd3'],
                                                 provides=['p1', 'p2'])

    def test_duplicated_task_addition(self, register):
        def func():
            pass

        register.add_handler(func.__name__, depends=[], provides=[])

        with pytest.raises(TaskAlreadyRegistered):
            register.add_handler(func.__name__, depends=[], provides=[])
