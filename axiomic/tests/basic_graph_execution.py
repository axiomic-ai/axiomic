
import axiomic
import axiomic.constants

import axiomic.core.checks as checks


def test_jsonschema_check():
    j = '"hello"'
    schema = '{"type": "string"}'
    check = axiomic.Text(j).check_jsonschema(schema)
    assert check.value() == axiomic.constants.TRUE_VALUE

def test_check_jsonschema():
    str_schema = '{"type": "string"}'

    assert axiomic.Text('"hello"').check(checks.CheckJsonSchema(str_schema)).value() == axiomic.constants.TRUE_VALUE
    assert checks.CheckJsonSchema(str_schema)('false').value() == axiomic.constants.FALSE_VALUE


def test_check_json_syntax():
    assert axiomic.Text('"hello"').check(checks.CheckJsonSyntax()).value() == axiomic.constants.TRUE_VALUE
    assert checks.CheckJsonSyntax()('"hello').value() == axiomic.constants.FALSE_VALUE
    assert axiomic.Text('{"hello": "goodbye"}').check(checks.CheckJsonSyntax()).value() == axiomic.constants.TRUE_VALUE
    assert axiomic.Text('{"hello": "goodbye",}').check(checks.CheckJsonSyntax()).value() == axiomic.constants.FALSE_VALUE

def test_json_syntax_thought_crime():
    try:
        # Expect to raise because "hello isn't value json.
        result = axiomic.Text('"hello').checkpoint(checks.CheckJsonSyntax()).value()
        assert False
    except axiomic.ThoughtCrime:
        assert True
