import os

from config import MobileApiConfig
from src.database import PostgresConnector
from src.api.factory import Factory
from src.api.factory.app_routes import mobile_routes

db = PostgresConnector(MobileApiConfig.DATABASE_URI)
factory = Factory('WEB_API', config=MobileApiConfig, routes=mobile_routes, db=db)
app = factory.create_app()
if __name__ == '__main__':
    host = '127.0.0.1'
    port = 8080
    app.run(host=host, port=port)
