from inspect import isfunction
from imgrabber.register import Register
from imgrabber.exceptions import TaskDependencyError


class Pipeline(object):
    def __init__(self, first_task, *tasks):
        if len(self._get_depends(first_task)) > 0:
            raise TaskDependencyError("First task can't have dependencies")

        self._tasks = [first_task] + list(tasks)

        for task in self._tasks:
            if not isfunction(task):
                raise ValueError("Task must be a function")
            if not self._is_applied(task):
                raise ValueError(
                    "Task must be applied before adding to pipeline")

            depends = self._get_depends(task)
            for dep in depends:
                if not self._is_dependency_satisfied(dep):
                    raise TaskDependencyError("Dependency {} of task {}" \
                        "is not satisfied".format(task.__name__, dep))

    def _is_applied(self, task):
        return hasattr(task, '_applied')

    def _get_depends(self, task):
        return Register().get_depends(task.__name__)

    def _get_provides(self, task):
        return Register().get_provides(task.__name__)

    def _add_provider(self, dependency, task):
        self._providers[dependency] = task

    def _is_dependency_satisfied(self, dependency):
        return (dependency in self._providers)

    @property
    def tasks(self):
        return self._tasks
