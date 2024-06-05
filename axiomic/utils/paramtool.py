
import re


PARAM_BASE_PATTERN = r'P(?:\.[a-zA-Z0-9_]+)+'
PARAM_BASE_REGEX = re.compile(f'^{PARAM_BASE_PATTERN}$')
PARAM_IN_BRACKETS_REGX = re.compile(f'{{(?P<param_str>{PARAM_BASE_PATTERN})}}')


def is_param_name(thing: str) -> bool:
    return PARAM_BASE_REGEX.match(thing) is not None


def segment_param_name(param_name: str) -> list:
    return param_name.split('.')[1:]

def get_all_imbedded_params(text: str) -> list:
    if type(text) is not str:
        raise TypeError(f"Expected a string, got {type(text)}: {text}")
    hits = PARAM_IN_BRACKETS_REGX.findall(text)
    return [h for h in hits]
