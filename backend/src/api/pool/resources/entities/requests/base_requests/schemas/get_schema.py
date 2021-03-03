from abc import abstractmethod

from marshmallow import fields, ValidationError, validates

from . import BaseSchema


class GetSchema(BaseSchema):
    id = fields.Integer(validate=lambda n: n >= 0)
    limit = fields.Integer(validate=lambda n: n > 0)
    offset = fields.Integer(validate=lambda n: n >= 0)
    order = fields.String(validate=lambda order: order in ['asc', 'desc'])
    sort = fields.String()
    relations = fields.List(fields.String())

    @validates('sort')
    def validate_sort(self, sort):
        if sort not in self.sort_rule():
            raise ValidationError('Invalid sort.')

    @validates('relations')
    def validate_relations(self, relations):
        errors = []
        for relation in relations:
            if relation not in self.relation_rule():
                errors.append('Invalid on relation: {}.'.format(relation))
        if errors:
            raise ValidationError(errors)

    @staticmethod
    @abstractmethod
    def sort_rule() -> list:
        pass

    @staticmethod
    @abstractmethod
    def relation_rule() -> list:
        pass
