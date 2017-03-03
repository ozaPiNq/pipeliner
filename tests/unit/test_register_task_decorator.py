import pytest

from pipeliner.register import task


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
        def test_task(context, p1, p2=None):
            context['p1'] = p1
            context['p2'] = p2

        register.get_handler('test_task')

        new_context = test_task(1, 2)(context)

        assert new_context['p1'] == 1
        assert new_context['p2'] == 2

    def test_registered_with_depends_and_provides(self, register, context):
        @task(depends=['1'], provides=['2'])
        def test_task(context, p1, p2=None):
            context['p1'] = p1
            context['p2'] = p2

        register.get_handler('test_task')

        new_context = test_task(1, 2)(context)

        assert new_context['p1'] == 1
        assert new_context['p2'] == 2


class TestTaskContextWrapperUpdate(object):
    def test_func_name_restore(self):
        @task()
        def test_func(context): pass

        assert test_func.__name__ == 'test_func'

        test_task = test_func()

        assert test_task.__name__ == 'test_func'

    def test_context_wrapper_returns_context(self, context):
        @task()
        def test_func(context):
            context['test'] = 1

        test_task = test_func()

        new_context = test_task(context)

        assert new_context['test'] == 1
