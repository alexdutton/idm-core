from django.core import exceptions
import jsonschema
from rest_framework.fields import JSONField


class JSONSchemaField(JSONField):
    def __init__(self, *args, schema, **kwargs):
        self._schema = schema
        super().__init__(*args, **kwargs)

    def validate(self, value, model_instance):
        super().validate(value, model_instance)
        try:
            jsonschema.validate(value, self._schema)
        except jsonschema.ValidationError as e:
            raise exceptions.ValidationError(
                self.error_messages['invalid'],
                code='invalid',
                params={'value': value},
            ) from e
