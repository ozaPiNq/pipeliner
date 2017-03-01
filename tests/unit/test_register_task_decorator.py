import pytest

from imgrabber.register import task


class TestTaskDecorator(object):
    def test_register_simple_task(self, register):
        @task()
        def test_task(): pass

        register.get_handler('test_task')

    def test_register_task_with_depends_and_provides(self, register):
        @task(depends=['1', '2', '3'], provides=['4', '5', '6'])
        def test_task(): pass

        handler = register.get_handler('test_task')

        assert handler['depends'] == ['1', '2', '3']
        assert handler['provides'] == ['4', '5', '6']
