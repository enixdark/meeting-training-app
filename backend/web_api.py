import os

from config import WebApiConfig

from src.database import PostgresConnector
from src.api.factory import Factory
from src.api.factory.app_routes import web_routes
from src.message_queue.celery_factory import CeleryFactory
from src.message_queue.celery_factory.celery_tasks import celery_tasks

db = PostgresConnector(WebApiConfig.DATABASE_URI)
factory = Factory('WEB_API', config=WebApiConfig, routes=web_routes, db=db)
app = factory.create_app()

# create celery
celery_factory = CeleryFactory(flask_app=app, task_list=celery_tasks)
celery = celery_factory.create_app()

if __name__ == '__main__':
    host = '127.0.0.1'
    port = 8080
    app.run(host=host, port=port)
