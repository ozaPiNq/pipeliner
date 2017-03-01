from imgrabber.pipeline import Pipeline
from imgrabber.register import task


class TestBasicPipelineCreation(object):
    def test_single_task_pipeline(self, context):
        @task()
        def test_func(ctx):
            return ctx

        test_task = test_func()

        pipeline = Pipeline(test_task)

        assert pipeline.tasks == [test_task]

    def test_multi_task_pipeline(self):
        pass


class TestPipelineDependencyChecking(object):
    def test_single_task_without_dependencies(self):
        pass

    def test_single_task_with_dependencies(self):
        pass

    def test_multi_task_pipeline_with_correct_dependencies(self):
        pass

    def test_multi_task_pipeline_with_incorrect_dependencies(self):
        pass
