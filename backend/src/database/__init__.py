from abc import ABC, abstractmethod

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os


class DBConnector(ABC):
    Base = declarative_base()

    def __init__(self, database_uri):
        self.__engine = create_engine(database_uri, echo=False)
        self.Session = sessionmaker(bind=self.__engine)

    def get_session(self):
        session = self.Session()
        return session


class PostgresConnector(DBConnector):
    pass
