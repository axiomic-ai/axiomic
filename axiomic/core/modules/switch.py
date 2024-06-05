
from typing import List, Dict

import axiomic

import axiomic.errors as errors
import axiomic.core.modules.json_pattern as json_pattern
import axiomic.core.modules.enforce_jsonschema as enforce_jsonschema
import json

import axiomic.data.lists as lists


def _make_jsonschema_enum(elements: List[str]) -> str:
    '''
    Make a JSON schema enum from a list of strings.

    Args:
        elements: A list of strings.

    Returns:
        A JSON schema enum.
    '''
    schema = {"type": "string", "enum": list(map(lambda s: s.lstrip('"').rstrip('"'), list(elements)))}
    return json.dumps(schema)


def _map_to_chat_history(case_map: Dict[str, List[str]]) -> List:
    l = []
    for k, v in case_map.items():
        for i in v:
            l.append((i, f'"{k}"'))
    return l


class Switch:
    '''
    Switch on an input and choose a specific case, effecively a semantic switch statement.
    For example, use this to choose which agent to route to based on the user input.

    .. code-block:: python

            import axiomic.core.modules as modules

            EXAMPLES = [
                ('I need help with the product I bought', '"SUPPORT"'),
                ('It is not working.', '"SUPPORT"'),
                ('I want to buy a product', '"SALES"'),
                ('I just bought a product and I need help.', '"SALES"'),
                ('I need a refund.', '"SALES"'),
                ('I do not like you. Go away.', '"COMPLAINT"')
            ]

            switch = modules.Switch(EXAMPLES)
            switch.infer('I just bought a product and I need help.').print()

    Args:
        case_examples: A dictionary mapping case names to lists of examples for that case.
        instructions: (Optional) explanation of the cases and when to choose which case.

    '''

    def __init__(self, case_examples: lists.ChatListType, instructions: axiomic.TextType = None):
        self.case_examples = lists.ChatList(case_examples)
        self.cases = [ex.agent for ex in self.case_examples]
        self.json_schema = _make_jsonschema_enum(list(set(self.cases)))
        self.json_gate = enforce_jsonschema.EnforceJsonSchema(schema=self.json_schema)
        if instructions is None:
            self.route_map_desc = 'Given text, state which of these cases most closely applies:\n'
            for k in self.cases:
                self.route_map_desc += f'{k}\n'
        else:
            self.route_map_desc = instructions
    
        for ex in self.case_examples:
            if not ex.agent.strip().startswith('"') or not ex.agent.strip().endswith('"'):
                raise errors.WeaveError(f'Case name must be a JSON serialized string (quoted): expected "{ex.agent}" got: {ex.agent}')
        self.json_pattern = json_pattern.JsonPattern(chat_list=self.case_examples, json_schema=self.json_schema, pattern_desc=self.route_map_desc)
        
    def infer(self, switch_text):
        '''
        :param case: The name of the agent to route to.
        :return: The name of the agent to route to.
        '''
        st = axiomic.Text(switch_text)
        return self.json_pattern.infer(switch_text)

    def make_eval_varients(self):
        case_vars = self.case_examples.make_eval_varients()
        return [(case_vars[0], Switch(case_vars[1])) for case_vars in case_vars]




