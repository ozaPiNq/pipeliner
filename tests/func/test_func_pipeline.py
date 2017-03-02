import pytest
from imgrabber.pipeline import Pipeline
from imgrabber.register import task


class TestPipeline(object):
    def test_single_task_pipeline(self, mock):
        mock_func = mock()

        @task()
        def test_func(ctx): mock_func(ctx)

        test_task = test_func()
        pipeline = Pipeline(test_task)

        assert not mock_func.called

        pipeline.run(wait=True)

        assert mock_func.called

    @pytest.mark.xfail
    def test_multiple_tasks_pipeline(self, dumb_task, target_mock):
        mock1 = target_mock()
        mock2 = target_mock()
        mock3 = target_mock()
        task1 = dumb_task(mock=mock1)
        task2 = dumb_task(mock=mock2)
        task3 = dumb_task(mock=mock3)

        assert not (mock1 == mock2 == mock3)
        assert not (task1 == task2 == task3)

        pipeline = Pipeline(task1, task2, task3)
        pipeline.run()
        pipeline.wait_until_complete()

        assert mock1.is_called
        assert mock2.is_called
        assert mock3.is_called

    @pytest.mark.xfail
    def test_abnormal_pipeline_termination(self, dumb_task, target_mock,
                                           bad_task):
        mock1 = target_mock()
        mock2 = target_mock()
        mock3 = target_mock()
        task1 = dumb_task(mock=mock1)
        broken_task = bad_task(mock=mock2)
        task3 = dumb_task(mock=mock3)

        assert not (mock1 == mock2 == mock3)
        assert not (task1 == broken_task == task3)

        pipeline = Pipeline(task1, broken_task, task3)
        pipeline.run()
        pipeline.wait_until_complete()

        assert mock1.is_called
        assert mock2.is_called
        assert mock3.is_called == False


@pytest.mark.xfail
class TestPipelineDependencies(object):
    def test_single_task_without_deps(self, dep_task):
        task = dep_task(depends=[], provides=['something'])

        Pipeline(task)

    def test_single_task_with_deps(self, dep_task):
        task = dep_task(depends=['something'], provides=['nothing'])

        with pytest.raises(PipelineDependencyError):
            Pipeline(task)

    def test_multiple_tasks_correct_deps(self, dep_task):
        task1 = dep_task(depends=[], provides=['task1'])
        task2 = dep_task(depends=['task1'], provides=['task2'])
        task3 = dep_task(depends=['task2'], provides=['task3'])

        Pipeline(task1, task2, task3)

    def test_multiple_tasks_incorrect_deps(self, dep_task):
        task1 = dep_task(depends=[], provides=['task1'])
        task2 = dep_task(depends=['task2'], provides=['task3'])
        task3 = dep_task(depends=['task1'], provides=['task2'])

        Pipeline(task1, task2, task3)
