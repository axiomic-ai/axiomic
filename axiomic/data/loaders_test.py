import pytest
from unittest.mock import patch, mock_open
import json
import yaml

# Assuming your module is named 'my_module'
import axiomic.data.loaders as loaders

def test_read_unstructured_success():
    # Mock opening a file that is supposed to read text content
    mock_data = "this is my text"
    with patch("builtins.open", mock_open(read_data=mock_data)):
        # No exception means it passed
        assert loaders.read_text("file.txt") == "this is my text"


def test_read_structured_json_success():
    # Mock opening a file that is supposed to read text content
    mock_data = '["one", "two", "three"]'
    with patch("builtins.open", mock_open(read_data=mock_data)):
        # No exception means it passed
        assert loaders.read_structured("file.json") == ["one", "two", "three"]


def test_read_structured_yaml_success():
    # Mock opening a file that is supposed to read text content
    mock_data = yaml.dump(["one", "two", "three"])
    with patch("builtins.open", mock_open(read_data=mock_data)):
        # No exception means it passed
        assert loaders.read_structured("file.yaml") == ["one", "two", "three"]


def test_load_json_serialized():
    # Mock reading a valid list of strings
    mock_data = '[[1, 2, 3], [5]]'
    with patch("builtins.open", mock_open(read_data=mock_data)):
        # No exception means it passed
        assert list(loaders.load_serialized_jsons("file.json")) == ['[1, 2, 3]', '[5]']


def test_load_yaml_serialized_json():
    # Mock opening a file that is supposed to read text content
    mock_data = '''
-   - 1
    - 2
- two
- three
    '''
    with patch("builtins.open", mock_open(read_data=mock_data)):
        # No exception means it passed
        assert list(loaders.load_jsons_serialized("file.yaml")) == ["[1, 2]", '"two"', '"three"']


def test_load_chat_text_json():
    # Mock opening a file that is supposed to read text content
    mock_data = '''
[
    {"user": "Hello Agent!", "agent": "Hi Person!"},
    {"user": "What's 5 + 5?", "agent": "It's 10"}
]
    '''

    with patch("builtins.open", mock_open(read_data=mock_data)):
        # No exception means it passed
        assert loaders.load_chat_text("file.json").as_list() == [("Hello Agent!", "Hi Person!"), ("What's 5 + 5?", "It's 10")]


def test_load_chat_text_yaml():
    # Mock opening a file that is supposed to read text content
    mock_data = '''
        - user: Hello Agent!
          agent: Hi Person!
        - user: What's 5 + 5?
          agent: It's 10
    '''

    with patch("builtins.open", mock_open(read_data=mock_data)):
        # No exception means it passed
        assert loaders.load_chat_text("file.yaml").as_list() == [("Hello Agent!", "Hi Person!"), ("What's 5 + 5?", "It's 10")]


def test_load_chat_serialized_json_json():
    # Mock opening a file that is supposed to read text content
    mock_data = '''
[
    {"user": {"a": 1}, "agent": {"b": 2}},
    {"user": {"a": 2}, "agent": {"b": 3}}
]
    '''

    schema = '{"type": "object"}'

    with patch("builtins.open", mock_open(read_data=mock_data)):
        # No exception means it passed
        assert loaders.load_chat_json_serialized("file.json", user_schema=schema, agent_schema=schema).as_list() == [('{"a": 1}', '{"b": 2}'), ('{"a": 2}', '{"b": 3}')]
    


