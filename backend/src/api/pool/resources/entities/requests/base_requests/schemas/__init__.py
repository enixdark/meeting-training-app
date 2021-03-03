from marshmallow import Schema
import copy


class BaseSchema(Schema):
    def __init__(self, *args, **kwargs):
        super(BaseSchema, self).__init__(*args, **kwargs)
        self.__init_args = args
        self.__init_kwargs = kwargs

    def load(self, data):
        clone_fields = copy.deepcopy(self.fields)
        clone_schema = self.__clone(self.__create_attributes(clone_fields), *self.__init_args, **self.__init_kwargs)

        super_load_result_errors = super(BaseSchema, self).load(data).errors
        clone_load_result = clone_schema.load(data)

        clone_load_result.errors.update(super_load_result_errors)
        return clone_load_result

    def __create_attributes(self, fields: dict):
        required_attributes = self._create_required_attributes()
        default_attributes = self._create_default_attributes()

        recreated_attributes = [
            *required_attributes,
            *default_attributes
        ]

        if len(recreated_attributes) > 0:
            required_dict = self.__set_required_attributes(fields)
            default_dict = self.__set_default_attributes(fields)

            for attribute in recreated_attributes:
                attribute_schema_kwargs = {
                    **required_dict.get(attribute, {}),
                    **default_dict.get(attribute, {}),
                }
                field_type = type(fields[attribute])
                fields[attribute] = field_type(**attribute_schema_kwargs)

        return fields

    def __set_required_attributes(self, fields: dict) -> dict:
        requires = {}
        required_attributes = self._create_required_attributes()
        for attribute in required_attributes:
            attribute_type = type(fields[attribute])
            if attribute_type:
                requires.update({
                    attribute: {
                        'required': True
                    }
                })
        return requires

    def __set_default_attributes(self, fields: dict) -> dict:
        default = {}
        default_attributes = self._create_default_attributes()
        for default_attribute, default_value in default_attributes.items():
            attribute_type = type(fields[default_attribute])
            if attribute_type:
                default.update({
                    default_attributes: {
                        'default': default_value
                    }
                })
        return default

    @classmethod
    def __clone(cls, fields: dict, *args, **kwargs) -> Schema:
        clone_type = type('{}Clone'.format(cls.__name__), (Schema,), fields)
        return clone_type(*args, **kwargs)

    @staticmethod
    def _create_required_attributes() -> list:
        return []

    @staticmethod
    def _create_default_attributes() -> dict:
        return {}
