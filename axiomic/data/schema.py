
import json
import typing
import jsonschema


def _to_schema_dict(schema: typing.Union[str, dict]):
    if isinstance(schema, dict):
        return schema
    return json.loads(schema)


class JsonSchema:
    
    def __init__(self, schema: typing.Union[str, dict]):
        self.schema = _to_schema_dict(schema)

    def validate(self, thing: any) -> bool:
        try:
            jsonschema.validate(thing, self.schema)
            return True
        except jsonschema.ValidationError:
            return False
        except jsonschema.SchemaError:
            return False

    def validate_serialized(self, thing: str) -> bool:
        try:
            jsonschema.validate(json.loads(thing), self.schema)
            return True
        except jsonschema.ValidationError:
            return False
        except jsonschema.SchemaError:
            return False
