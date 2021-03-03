from abc import abstractmethod
from datetime import datetime

from celery.task import Task


class BaseMeetingTask(Task):

    @abstractmethod
    def run(self, *args, **kwargs):
        pass

    def _create_task_name(self) -> str:
        return '{class_name}-task-{date}'.format(class_name=type(self).__name__,
                                                 date=datetime.now().isoformat())

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        print('{0!r} failed: {1!r}'.format(task_id, exc))
