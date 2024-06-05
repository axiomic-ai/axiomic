
import jsonschema 
import axiomic.errors as errors
import axiomic.constants as constants
import axiomic.utils.wjson as wjson
import axiomic.protos as protos
import json


CHECKS = {}


def register_check(name):
    def wrapper(func):
        CHECKS[name] = func
        return func
    return wrapper


@register_check(protos.axiomic.BuiltinBinaryCheckNode.CHECK_JSONSCHEMA)
def check_json_schema(json_str: str, json_schema: str) -> str:
    parse_ok = False
    try:
        jo = wjson.loads(json_str) 
        parse_ok = True
    except json.decoder.JSONDecodeError as e:
        pass

    if not parse_ok:
        raise errors.WeaveError('Ask to validate a JSON schema (did you forget to check json syntax first?) on a non-JSON string: ' + json_str)

    parse_ok = False
    try:
        schema = wjson.loads(json_schema)
        parse_ok = True
    except json.decoder.JSONDecodeError:
        pass

    if not parse_ok:
        raise errors.WeaveError('Schema is not valid JSON: ' + json_schema)

    try:
        jsonschema.validate(jo, schema)
        return constants.TRUE_VALUE
    except jsonschema.exceptions.ValidationError as e:
        print('/' * 80)
        print(e)
        print('\\' * 80)
    except jsonschema.exceptions.SchemaError as e:
        print('/' * 80)
        print(e)
        print('\\' * 80)
        raise errors.WeaveError('Schema is not a valid schema: ' + json_schema)

    return constants.FALSE_VALUE
