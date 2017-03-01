import pytest

from imgrabber.register import task


class TestTaskDecorator(object):
    def test_register_simple_task(self, register):
        @task
        def test_task(context): pass

        register.get_handler('test_task')
