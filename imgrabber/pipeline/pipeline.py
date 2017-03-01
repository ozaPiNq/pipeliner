class Pipeline(object):
    def __init__(self, first_task, *tasks):
        self._tasks = [first_task] + list(tasks)

    @property
    def tasks(self):
        return self._tasks
