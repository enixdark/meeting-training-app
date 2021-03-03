from celery import Celery
from celery.task import Task
from flask import Flask


class CeleryFactory:
    def __init__(self, flask_app: Flask, task_list: list):
        self.__flask_app = flask_app
        self.__task_list = task_list

    def create_app(self):
        celery_app = Celery(self.__flask_app.name, broker=self.__flask_app.config['CELERY_BROKER_URL'])

        # config celery with flask config
        celery_app.conf.update(self.__flask_app.config)

        # register custom tasks
        celery_app = self.__register_service_task(celery_app, self.__task_list)
        
        return celery_app

    @staticmethod
    def __register_service_task(celery_app, service_task: list):
        for task in service_task:
            if isinstance(task, Task):
                celery_app.register_task(task)
        return celery_app
