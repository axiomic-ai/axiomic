
import json
import typing
import jsonschema
import axiomic.frontend.text as text


JsonSchemaType = typing.Union[str, dict]


def _to_schema_dict(schema: JsonSchemaType):
    if isinstance(schema, dict):
        return schema
    # Pass through parameter expansion
    return json.loads(Text(schema).value())


class ValidatorString:
    def validate(self, thing: any) -> bool:
        return isinstance(thing, str)


class ValidateSerializedJson:
    def validate(self, thing: any) -> bool:
        try:
            json.loads(thing)
            return True
        except json.JSONDecodeError:
            return False


class ValidatorJson:
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


class ValidatorJsonSchemaSerialized:
    def __init__(self, schema: typing.Union[str, dict]):
        self.schema = _to_schema_dict(schema)
        
    def validate(self, thing: str) -> bool:
        try:
            jsonschema.validate(json.loads(thing), self.schema)
            return True
        except jsonschema.ValidationError:
            return False
        except jsonschema.SchemaError:
            return False


class ValidatorPydantic:
    def __init__(self, pydantic_model: any):
        self.pydantic_model = pydantic_model
        
    def validate(self, thing: any) -> bool:
        return isinstance(thing, self.pydantic_model)


class Validator:
    def __init__(self, validator: any):
        self.validator = validator

