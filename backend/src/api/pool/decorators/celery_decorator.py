from abc import ABC

from src.api.pool.services import Service
from src.message_queue.tasks import BaseMeetingTask
from .auth_decorator import AuthenticatedDecorator


class CeleryDecorator(AuthenticatedDecorator, ABC):
    def __init__(self):
        super().__init__()
        self.tasks = []

    def _add_executor(self, task: BaseMeetingTask, delay_arguments=None, async_options=None):
        """
        Add BaseMeetingTask instance to self.__executor list
        :param task: BaseMeetingTask instance, that execute activities asynchronously.
        :param delay_arguments: Kwargs for task's run function
        :param async_options: Async options for task's apply_async function
        :return: None
        """
        if not isinstance(delay_arguments, dict):
            delay_arguments = {}
        if not isinstance(async_options, dict):
            async_options = {}

        task = {
            'task': task,
            'delay_arguments': delay_arguments,
            'async_options': async_options
        }
        self.tasks.append(task)

    def _execute(self):
        """
        Execute the task with related arguments and options.
        :return: None
        """
        for task in self.tasks:
            task['task'].apply_async(kwargs=task['delay_arguments'], **task['async_options'])

        # empty task list after execute
        self._flush_tasks()

    def _execute_chain(self):
        """
        Execute the chain of task with related arguments and options.
        :return: None
        """
        custom = []
        for task in self.tasks:
            custom.append(task['task'].s(**task['delay_arguments']))
        if len(custom) > 0:
            from celery import chain
            chain(*custom).apply_async(**self.tasks[0]['async_options'])

        # empty task list after execute
        self._flush_tasks()

    def _flush_tasks(self):
        # empty task list after execute
        self.tasks = []

    def _create_service(self) -> Service:
        pass
