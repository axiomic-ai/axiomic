
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


@register_check(protos.axiomic.BuiltinUnaryCheckNode.CHECK_JSON_SYNTAX)
def check_json_syntax(json_str: str) -> str:
    parse_ok = False
    try:
        jo = wjson.loads(json_str) 
        return constants.TRUE_VALUE
    except json.decoder.JSONDecodeError as e:
        pass

    return constants.FALSE_VALUE

