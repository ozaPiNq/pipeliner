from inspect import isfunction


class Pipeline(object):
    def __init__(self, first_task, *tasks):
        self._tasks = [first_task] + list(tasks)
        for task in self._tasks:
            if not isfunction(task):
                raise ValueError("Task must be a function")
            if not self._is_applied(task):
                raise ValueError(
                    "Task must be applied before adding to pipeline")

    def _is_applied(self, task):
        return hasattr(task, '_applied')

    @property
    def tasks(self):
        return self._tasks
