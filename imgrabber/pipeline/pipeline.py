from inspect import isfunction


class Pipeline(object):
    def __init__(self, first_task, *tasks):
        self._tasks = [first_task] + list(tasks)
        for task in self._tasks:
            if not isfunction(task):
                raise ValueError("Task must be a function")

    @property
    def tasks(self):
        return self._tasks
