from abc import ABC, abstractmethod

from src.database.postgres.base import Model
from flask import g


class Service(ABC):
    @abstractmethod
    def create_new_model(self, *args, **kwargs) -> Model:
        pass

    @abstractmethod
    def update_model(self, *args, **kwargs) -> bool:
        pass

    @abstractmethod
    def find_model(self, pairs: dict, **kwargs) -> Model:
        pass

    @abstractmethod
    def delete_model(self, *args, **kwargs) -> bool:
        pass

    @abstractmethod
    def get_model(self, _id, **kwargs) -> Model:
        pass

    @abstractmethod
    def get_all(self, *args, **kwargs):
        pass


class BaseService(Service, ABC):
    def __init__(self):
        self._class = self._create_class_model()
        self.session = self.create_session()
        self.__model = None

    @abstractmethod
    def _create_class_model(self):
        pass

    @abstractmethod
    def create_session(self):
        pass

    def create_many_to_many_relations(self) -> dict:
        return {}

    def _set_model(self, model: Model):
        self.__model = model

    def _save_model(self) -> bool:
        self.session.add(self.__model)
        return True

    def _delete_model(self) -> bool:
        self.session.delete(self.__model)
        return True

    def create_new_model(self, *args, **kwargs) -> Model:
        if self._save_model():
            return self.__model

    def update_model(self, *args, **kwargs) -> bool:
        relations = self.create_many_to_many_relations()
        for k, v in kwargs.items():
            if k in relations.keys():
                self._sync(relation_type_name=relations[k], values=v)
            else:
                setattr(self.__model, k, v)
        return self._save_model()

    def _sync(self, relation_type_name, values):
        relation_type = getattr(type(self.__model), relation_type_name).property.mapper.class_
        relation_values = []
        for relation_value in values:
            relation_values.append(relation_type(**relation_value))
        setattr(self.__model, relation_type_name, relation_values)

    def find_model(self, pairs: dict, **kwargs) -> Model:
        query = self.session.query(self._class)
        if len(pairs) > 0:
            for key, value in pairs.items():
                pair = {key: value}
                query = query.filter_by(**pair)

            return query.first()

    def delete_model(self, *args, **kwargs) -> bool:
        return self._delete_model()

    def get_model(self, _id, **kwargs) -> Model:
        return self.session.query(self._class).get(_id)

    def get_all(self, *args, **kwargs):
        sort = kwargs.get('sort', None)
        order = kwargs.get('order', None)
        offset_n = kwargs.get('offset', None)
        limit_n = kwargs.get('limit', None)

        query = self.session.query(self._class)
        if sort:
            if order == 'desc':
                from sqlalchemy import desc
                query = query.order_by(desc(sort))
            query = query.order_by(sort)
        if offset_n:
            query = query.offset(offset_n)
        if limit_n:
            query = query.limit(limit_n)

        return query.all()


class FlaskBaseService(BaseService, ABC):
    def create_session(self):
        if g:
            return g.session


class FormService(FlaskBaseService, ABC):
    """
        CRUD Service that allows search model by id
        Used by decorators to create multi-steps transactions
        Do not use its subclasses to inject into resource classes because of ambiguity commit activities
    """

    def create_new_model(self, *args, **kwargs) -> Model:
        # print('here', self._class, kwargs)
        new_model = self._class(**kwargs)
        self._set_model(new_model)
        return super().create_new_model()

    def update_model(self, _id, **kwargs) -> bool:
        updated_model = self.get_model(_id)
        if updated_model:
            self._set_model(updated_model)
            return super().update_model(**kwargs)
        return False

    def delete_model(self, _id, **kwargs) -> bool:
        deleted_model = self.get_model(_id)
        if deleted_model:
            self._set_model(deleted_model)
            return super().delete_model()
        return False


class InstantFormService(FormService, ABC):
    """
        CRUD FormService that commits right after adds model to session.
        Used by resources that executes add-and-commit transactions
    """

    def _save_model(self) -> bool:
        super()._save_model()
        return self.__instant_commit()

    def _delete_model(self) -> bool:
        super()._delete_model()
        return self.__instant_commit()

    def __instant_commit(self) -> bool:
        try:
            self.session.commit()
        except Exception as e:
            print(e)
            self.session.rollback()
            return False
        return True


class DecoratorService(FlaskBaseService, ABC):
    """
        CRUD Service that allows search model by passing to parameter
        Used by decorators to create multi-steps transactions
        Do not use its subclasses to inject into resource classes because of ambiguity commit activities
    """

    def create_new_model(self, new_model: Model, **kwargs) -> Model:
        self._set_model(new_model)
        if super().create_new_model(**kwargs):
            return new_model

    def update_model(self, updated_model, **kwargs) -> bool:
        self._set_model(updated_model)
        if super().update_model(**kwargs):
            return super()._save_model()

    def delete_model(self, deleted_model, **kwargs) -> bool:
        self._set_model(deleted_model)
        return super().delete_model()
