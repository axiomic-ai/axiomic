
import axiomic

import axiomic.protos as protos


def _unary_check(cls):
    def is_core_unary_check(self) -> bool:
        return True
    cls.is_core_unary_check = is_core_unary_check
    def is_core_binary_check(self) -> bool:
        return False
    cls.is_core_binary_check = is_core_binary_check
    def get_core_unary_check_code(self) -> int:
        return self.check_code
    cls.get_core_unary_check_code = get_core_unary_check_code
    def get_core_binary_check_code(self) -> int:
        raise ValueError('This is not a binary check.')
    cls.get_core_binary_check_code = get_core_binary_check_code
    def get_input_secondary(self) -> axiomic.TextType:
        raise ValueError('This is not a binary check.')
    cls.get_input_secondary = get_input_secondary
    return cls
    

def _binary_check(cls):
    def is_core_unary_check(self) -> bool:
        return False
    cls.is_core_unary_check = is_core_unary_check
    def is_core_binary_check(self) -> bool:
        return True
    cls.is_core_binary_check = is_core_binary_check
    def get_core_unary_check_code(self) -> int:
        raise ValueError('This is not a unary check.')
    def get_core_binary_check_code(self) -> int:
        return self.check_code
    cls.get_core_binary_check_code = get_core_binary_check_code
    def get_input_secondary(self) -> axiomic.TextType:
        return self.input_secondary 
    cls.get_input_secondary = get_input_secondary
    return cls


@_unary_check
class CheckJsonSyntax:
    def __init__(self):
        self.check_code = protos.axiomic.BuiltinUnaryCheckNode.CHECK_JSON_SYNTAX
    
    def __call__(self, possibly_json: axiomic.TextType) -> axiomic.Text:
        '''
        Check if the input is valid JSON.

        Args:
            possibly_json: A string that may be valid JSON.

        Returns:
            Text which represents if the input is valid JSON.
        '''
        return axiomic.Text(possibly_json).check(self)


@_binary_check
class CheckJsonSchema:
    def __init__(self, schema: axiomic.TextType):
        self.input_secondary = schema
        self.check_code = protos.axiomic.BuiltinBinaryCheckNode.CHECK_JSONSCHEMA

    def __call__(self, json_object: axiomic.TextType) -> axiomic.Text:
        '''
        Check if the input is valid JSON.

        Args:
            json_object: A string that may be valid JSON.
            schema: A string that may be valid JSON schema.

        Returns:
            Text which represents if the input is valid JSON.
        '''
        return axiomic.Text(json_object).check(self)
    