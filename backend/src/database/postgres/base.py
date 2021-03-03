import datetime
from abc import abstractmethod

from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.ext.declarative import declared_attr, declarative_base

Base = declarative_base()


class Model(object):
    @declared_attr
    def __tablename__(cls):
        return ''.join('_%s' % c if c.isupper() else c
                       for c in cls.__name__).strip('_').lower()

    # __abstract__ = True
    __table_args__ = {'useexisting': True}

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, onupdate=datetime.datetime.now)

    def serialize(self, **kwargs) -> dict:
        exclusion = kwargs.get('exclusion', [])
        inclusion_rs = kwargs.get('inclusion_rs', [])
        valid_relation_keys = self._relation_keys()

        accepted_relation_keys = [key for key in inclusion_rs if key in valid_relation_keys]

        to_dict = self._to_dict()
        to_dict = self.__remove_requirements(requirements=exclusion, serialize_model=to_dict)
        to_dict = self.__add_relationships(relationships=accepted_relation_keys, serialize_model=to_dict)
        to_dict = self.__add_common_fields(to_dict)

        return to_dict

    @staticmethod
    def __remove_requirements(requirements: [], serialize_model: dict) -> dict:
        if len(requirements) > 0:
            to_dict_keys = serialize_model.keys()
            needless = [key for key in requirements if key in to_dict_keys]
            for key in needless:
                del serialize_model[key]
        return serialize_model

    def __add_relationships(self, relationships: [], serialize_model: dict) -> dict:
        for relationship in relationships:
            method_to_call = getattr(self, '_{}'.format(relationship))
            serialize_model.update({relationship: method_to_call()})
        return serialize_model

    def __add_common_fields(self, serialize_model: dict):
        serialize_model.update({'created_at': self.created_at.isoformat()})
        if self.updated_at:
            serialize_model.update({'updated_at': self.updated_at.isoformat()})
        else:
            serialize_model.update({'updated_at': self.created_at.isoformat()})
        return serialize_model

    @abstractmethod
    def _to_dict(self) -> dict:
        pass

    @abstractmethod
    def _relation_keys(self) -> list:
        pass
