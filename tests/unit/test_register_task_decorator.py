import pytest

from imgrabber.register import task


class TestSimpleTaskDecorator(object):
    def test_registered(self, register, context):
        @task()
        def test_task(context): return context

        register.get_handler('test_task')

        assert test_task()(context) == context

    def test_registered_with_depends_and_provides(self, register, context):
        @task(depends=['1', '2', '3'], provides=['4', '5', '6'])
        def test_task(context): return context

        handler = register.get_handler('test_task')

        assert test_task()(context) == context

        assert handler['depends'] == ['1', '2', '3']
        assert handler['provides'] == ['4', '5', '6']


class TestTaskWithParamsDecorator(object):
    def test_registered(self, register, context):
        @task()
        def test_task(context, p1, p2, p3=None, p4=None):
            return (context, p1, p2, p3, p4)

        register.get_handler('test_task')

        assert test_task(1, 2, 3, 4)(context) == (context, 1, 2, 3, 4)

    def test_registered_with_depends_and_provides(self, register, context):
        @task(depends=['1'], provides=['2'])
        def test_task(context, p1, p2=None): return (context, p1, p2)

        register.get_handler('test_task')

        assert test_task(1, 2)(context) == (context, 1, 2)
