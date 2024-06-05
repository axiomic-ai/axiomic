
import axiomic.data.lists as lists

import axiomic.models as wc
import collections

import json
import yaml
import jsonschema
import pydantic

import axiomic.data.validate as validate


LIST_OF_STRINGS_SCHEMA = {'type': 'array', 'items': {'type': 'string'}}
LIST_SCHEMA = {'type': 'array'}

CHAT_SCHEMA = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "user": {
                "type": "string"
            },
            "agent": {
                "type": "string"
            }
        },
        "required": ["user", "agent"]
    }
}

CHAT_SCHEMA_STRUCT = {
    "type": "array",
    "items": {
        "type": "object",
        "required": ["user", "agent"]
    }
}


def _read(filename: str) -> any:
    filename = wc.resolve_axiomic_variables(filename)
    if '$' in filename:
        raise ValueError(f'Failed to resolve axiomic variables in filename: {filename}')

    with open(filename, 'r') as f:
        return f.read()


def read_text(filename: str) -> str:
    '''
    Reads a file and returns the contents as a string.

    Only reads .txt files.

    Will do axiomic variable expansion in the filename,
    e.g. `read_text('$axiomic_DATA_ROOT/file.txt')`.

    Args:
        filename (str): The filename to read.

    Returns:
        The contents of the file as a string.
    '''
    contents = _read(filename)
    # fail if structured
    if filename.endswith('.json') or filename.endswith('.yaml'):
        raise ValueError(f'Expected text file (.txt): {filename}')
    return contents


def read_structured(filename: str) -> any:
    contents = _read(filename)

    if filename.endswith('.json'):
        return json.loads(contents)
    if filename.endswith('.yaml'):
        return yaml.load(contents, Loader=yaml.FullLoader)
    raise ValueError(f'Unsupported file type (execpted .json, .yaml): {filename}')


def _check_schema(filename, data, schema):
    jsonschema.validate(instance=data, schema=schema)


def load_strings(filename: str) -> lists.TextList:
    '''
    Loads a list of strings from a file.


    Example, `file.json` contains:
    ```
        [
            "one",
            "two"
        ]
    ```
    Or `file.yaml` contains:
    ```
        - one
        - two
    ```

    Loads as this structure:
    ```
        axiomic.data.TextList(["one", "two"])
    ```

    Args:
        filename (str): The filename to load.

    Returns:
        A TextList of strings.
    '''
    result = read_structured(filename)
    _check_schema(filename, result, LIST_OF_STRINGS_SCHEMA)
    return lists.TextList(result)


def load_jsons_parsed(filename: str, schema: str = None) -> lists.TextList:
    '''
    Loads a file as a TextList of jsons. The JSONs are deserialized.

    Can load either a YAML or JSON file.

    Example, `file.json` contains:
    ```
        [
            {"a": 1, "b": 2},
            {"a": 3, "b": 4}]
        ]
    ```
    Or `file.yaml` contains:
    ```
        - a: 1
          b: 2
        - a: 3
          b: 4
    ```

    Loads as this structure:
    ```
        axiomic.data.TextList([{"a": 1, "b": 2}, {"a": 3, "b": 4}])
    ```

    Parameters:
        filename (str): The filename to load.
        schema (str): Optional, the schema to validate the JSONs against.

    Returns:
        A TextList of unserialize JSON objects.
    '''
    result = read_structured(filename)
    if schema is not None:
        _check_schema(filename, result, LIST_SCHEMA)
    return lists.TextList(result)


def load_jsons_unparsed(filename: str, schema: str = None) -> lists.TextList:
    '''
    Loads a file as a TextList of jsons. The JSONs are not deserialized.

    Can load either a YAML or JSON file.

    Example, `file.json` contains:
    ```
        [
            {"a": 1, "b": 2},
            {"a": 3, "b": 4}]
        ]
    ```
    Or `file.yaml` contains:
    ```
        - a: 1
          b: 2
        - a: 3
          b: 4
    ```

    Loads as this structure:
    ```
        axiomic.data.TextList(['{"a": 1, "b": 2}', '{"a": 3, "b": 4}'])
    ```

    Parameters:
        filename (str): The filename to load.
        schema (str): Optional, the schema to validate the JSONs against.

    Returns:
        A TextList of serialized JSON objects.
    '''
    result = read_structured(filename)
    if schema is not None:
        _check_schema(filename, result, schema)
    l = []
    for s in result:
        l.append(json.dumps(s))
    return lists.TextList(l)


def load_pydantics(filename: str, pydantic_model: pydantic.BaseModel) -> lists.TextList:
    jsons = load_jsons_parsed(filename)

    pydantics = []
    for j in jsons:
        pydantics.append(pydantic_model(**j))

    return lists.TextList(pydantics)


def load_chat_text(filename: str, strip=True) -> lists.ChatList:
    '''
    Loads a chat from a file.

    Example, `file.json` contains:
    ```
        [
            {"user": "Hello Agent!", "agent": "Hi Person!"},
            {"user": "What's 5 + 5?", "agent": "It's 10"},
        ]
    ```
    Or `file.yaml` contains:
    ```
        - user: Hello Agent!
          agent: Hi Person!
        - user: What's 5 + 5?
          agent: It's 10
    ```

    Loads as this structure:
    ```
        axiomic.data.ChatList([("Hello Agent!", "Hi Person!"), ("What's 5 + 5?", "It's 10")])
    ```

    Args:
        filename (str): The filename to load.
        strip (bool): If True, strip whitespace from the user and agent strings.

    Returns:
        A axiomic.data.ChatList.
    '''
    result = read_structured(filename)
    _check_schema(filename, result, CHAT_SCHEMA)
    pairs = [(d['user'], d['agent']) for d in result]

    if strip:
        pairs = [(user.strip(), agent.strip()) for user, agent in pairs]

    return lists.ChatList(pairs)


def load_chat_jsons_unparsed(filename: str, user_schema: validate.JsonSchemaType, agent_schema: validate.JsonSchemaType, strip=True) -> lists.ChatList:
    '''
    Loads a chat from file, validating if the user and agent strings are valid JSON.

    Example, if `file.json` contains:
    ```
        [
            {"user": {"a": 1}, "agent": {"b": 2}},
            {"user": {"a": 2}, "agent": {"b": 3}},
        ]
    ```
    Becomes:
    ```
        axiomic.data.ChatList([('{"a": 1}', '{"b": 2}'), ('{"a": 2}', '{"b": 3}')]
    ```

    Args:
        filename (str): The filename to load.
        user_schema (any): A custom validator to validate the user strings.
        agent_schema (any): A custom validator to validate the agent strings.

    Returns:
        A axiomic.data.ChatList.
    '''
    parsed = load_chat_jsons_parsed(filename, user_schema, agent_schema, strip)
    unparsed = []
    for chat in parsed:
        unparsed.append((json.dumps(chat.user), json.dumps(chat.agent)))
    return lists.ChatList(unparsed)


def load_chat_jsons_parsed(filename: str, user_schema: validate.JsonSchemaType, agent_schema: validate.JsonSchemaType, strip=True) -> lists.ChatList:
    read = read_structured(filename)
    _check_schema(filename, read, CHAT_SCHEMA_STRUCT)

    def strip_if_string(text):
        if not strip:
            return text
            
        if isinstance(text, str):
            return text.strip()
        return text

    pairs = [(strip_if_string(d['user']), strip_if_string(d['agent'])) for d in read]
    serialized = []
    user_validator = validate.ValidatorJson(user_schema)
    agent_validator = validate.ValidatorJson(agent_schema)
    for user, agent in pairs:
        new_user = None
        new_agent = None
        user_validator.validate(user)
        agent_validator.validate(agent)
        serialized.append((user, agent))

    return lists.ChatList(serialized)


def load_chat_pydantic(filename: str, user_model: pydantic.BaseModel, agent_model: pydantic.BaseModel) -> lists.ChatList:
    user_schema = user_model.schema()
    agent_schema = agent_model.schema()
    parsed_chat = load_chat_jsons_parsed(filename, user_schema, agent_schema)

    pairs = []

    for c in parsed_chat:
        u = user_model(**c.user)
        a = agent_model(**c.agent)
        pairs.append((u, a))
    
    return lists.ChatList(pairs)

