
import axiomic

import axiomic.errors as errors
import axiomic.builtins.knits.pattern as pattern
import axiomic.builtins.knits.json_pattern as json_pattern 
import axiomic.builtins.knits.jsonschema_gate as jsonschema_gate

from weave import P

import json


class ListOfStrings:
    '''
    Converts which enbumerates a list of a list of strings.
    Ex.
    "I like apples and oranges" -> ["apples", "oranges"]
    '''

    def __init__(self):
        '''
        :param route_map: A dictionary mapping agent names to their descriptions.
        '''
        self.schema = P.builtin.jsonschema.string_list
        self.json_gate = jsonschema_gate.JsonSchemaGate(schema=self.schema)
        self.pattern_desc = P.builtin.contrib.uagent.list_of_strings.pattern_desc
        self.pattern = json_pattern.JsonPattern(pattern_desc=self.pattern_desc, json_schema=self.schema)

    def infer(self, text_list):
        '''
        :param case: The name of the agent to route to.
        :return: The name of the agent to route to.
        '''
        text_list = axiomic.Text(text_list)
        return self.pattern.infer(text_list)




