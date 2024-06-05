
import axiomic
from axiomic import P


def test_param_unweave():
    assert 'json-schema.org' in P.core.jsonschema.boolean.value()

def test_param_native_format():
    assert 'json-schema.org' in axiomic.Text(f'{P.core.jsonschema.boolean}').value()

def test_param_implied_format():
    assert 'json-schema.org' in axiomic.Text('{P.core.jsonschema.boolean}').value()





