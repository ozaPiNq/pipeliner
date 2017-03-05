import pytest

from pipeliner.pipeline import Pipeline
from pipeliner.register import task
from pipeliner.exceptions import TaskDependencyError


class TestBasicPipelineCreation(object):
    def test_single_task_pipeline(self, context):
        @task()
        def test_func(ctx):
            return ctx

        test_task = test_func()

        pipeline = Pipeline(test_task)

        assert pipeline.tasks == [test_task]

    def test_multi_task_pipeline(self):
        @task()
        def test_func1(ctx): return ctx

        @task()
        def test_func2(ctx): return ctx

        test_task1 = test_func1()
        test_task2 = test_func2()

        pipeline = Pipeline(test_task1, test_task2)

        assert pipeline.tasks == [test_task1, test_task2]

    def test_some_tasks_are_not_functions(self):
        @task()
        def test_func(ctx): return ctx

        class Task(object): pass

        with pytest.raises(ValueError):
            Pipeline(test_func(), test_func(), Task(), test_func())

    def test_some_tasks_were_not_applied(self):
        """ Check if Pipeline rejects not applied tasks """
        @task()
        def test_func(ctx): return ctx

        with pytest.raises(ValueError):
            # here we forgot to apply 3rd task
            Pipeline(test_func(), test_func(), test_func, test_func())


class TestPipelineDependencyChecking(object):
    @pytest.mark.xfail
    def test_task_was_not_registered(self):
        assert 0, 'write the test'

    def test_single_task_with_dependencies(self):
        """ Check if first task with dependencies will be rejected """
        @task(depends=['mega_task'])
        def test_func(ctx): return ctx

        with pytest.raises(TaskDependencyError) as exc_info:
            Pipeline(test_func())

        assert exc_info.value.message == ("Dependency `mega_task` of task "
                                          "`test_func` is not satisfied")

    def test_multi_task_pipeline_with_correct_dependencies(self):
        @task(depends=[], provides=['task1_result'])
        def test_func1(ctx): return ctx

        @task(depends=['task1_result'], provides=['task2_result'])
        def test_func2(ctx): return ctx

        @task(depends=['task2_result'], provides=[])
        def test_func3(ctx): return ctx

        Pipeline(test_func1(), test_func2(), test_func3())

    def test_multi_task_pipeline_with_incorrect_dependencies(self):
        @task(depends=[], provides=['task1_result'])
        def test_func1(ctx): return ctx

        @task(depends=['task1_result'], provides=['task2_result'])
        def test_func2(ctx): return ctx

        @task(depends=['unknown_task_result'], provides=[])
        def test_func3(ctx): return ctx

        with pytest.raises(TaskDependencyError) as exc_info:
            Pipeline(test_func1(), test_func2(), test_func3())

        assert exc_info.value.message == ('Dependency `unknown_task_result` of'
                                          ' task `test_func3` is not satisfied')

    def test_multi_task_pipeline_with_initialized_context(self):
        @task(depends=['input_value'], provides=['task1_result'])
        def test_func1(ctx): return ctx

        @task(depends=['task1_result'], provides=['task2_result'])
        def test_func2(ctx): return ctx

        @task(depends=['task2_result'], provides=[])
        def test_func3(ctx): return ctx

        Pipeline(
            test_func1(),
            test_func2(),
            test_func3(),
            input_value='testing',
        )


class TestPipelineRun(object):
    def test_run_single_task(self, mock, context):
        mock_func = mock()

        @task()
        def test_func(ctx, arg1, arg2):
            mock_func(ctx, arg1, arg2)

        pipeline = Pipeline(test_func(arg1='1', arg2='2'))
        pipeline.run(wait=True)

        assert mock_func.called == True
        mock_func.assert_called_with(context, '1', '2')

    def test_run_multiple_task(self, mock):
        mock_func1 = mock()
        mock_func2 = mock()
        mock_func3 = mock()

        @task()
        def test_func1(ctx):
            mock_func1(ctx)

        @task()
        def test_func2(ctx):
            mock_func2(ctx)

        @task()
        def test_func3(ctx):
            mock_func3(ctx)

        pipeline = Pipeline(test_func1(), test_func2(), test_func3())
        pipeline.run(wait=True)

        assert mock_func1.called == True
        assert mock_func2.called == True
        assert mock_func3.called == True

    def test_run_multiple_task_one_failed(self, mock):
        mock_func1 = mock()
        mock_func2 = mock()
        mock_func2.side_effect = Exception()
        mock_func3 = mock()

        @task()
        def test_func1(ctx):
            mock_func1(ctx)

        @task()
        def test_func2(ctx):
            mock_func2(ctx)

        @task()
        def test_func3(ctx):
            mock_func3(ctx)

        pipeline = Pipeline(test_func1(), test_func2(), test_func3())
        pipeline.run(wait=True)

        assert mock_func1.called == True
        assert mock_func2.called == True
        assert mock_func3.called == False


class TestPipelineContextInitialization(object):
    def test_init_pipeline_with_multiple_values(self, mock):
        mock_func = mock()

        @task()
        def test_task(context):
            mock_func(context)

        pipeline = Pipeline(test_task(), key='value', file='random_file')
        pipeline.run(wait=True)

        context = mock_func.call_args[0][0]

        assert context['key'] == 'value'
        assert context['file'] == 'random_file'


class TestPipelineSynchronization(object):
    def test_wait_for(self, mock):
        mock_func1 = mock()
        mock_func2 = mock()
        mock_func3 = mock()

        @task()
        def test_func(context, cb, time=1):
            from time import sleep
            sleep(time)
            cb()

        @task()
        def start_nested_pipeline(context):
            p1 = Pipeline(test_func(mock_func1, time=1))
            p2 = Pipeline(test_func(mock_func2, time=2))
            p3 = Pipeline(test_func(mock_func3, time=2))

            p1.run()
            p2.run()
            p3.run()

            context.current_pipeline.wait_for([p1, p2, p3])

        parent_pipeline = Pipeline(start_nested_pipeline())
        parent_pipeline.run(wait=True)

        assert mock_func1.called
        assert mock_func2.called
        assert mock_func3.called
