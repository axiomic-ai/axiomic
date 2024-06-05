

import json
import pydantic


def coerce_to_str(thing: any) -> str:
    '''
    Converts any object to a string.

    Args:
        thing (any): The object to convert.

    Returns:
        str: The string representation of the object.
    '''

    if thing is None:
        return None

    if isinstance(thing, pydantic.BaseModel):
        return str(thing.json())

    if type(thing) is str:
        return thing

    # assume it should be serialized to json
    return json.dumps(thing)
