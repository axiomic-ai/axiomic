
import axiomic
import axiomic.builtins.knits.jsonschema_gate as jsonschema_gate
import json


class StringListSort:
    def __init__(self, criteria, 
                 instruction_template: str = '{p/builtin:knits:list_sort_template}', 
                 sysprompt_template: str = '{p/builtin:knits:list_sort_sysprompt}'):
        self.criteria = criteria
        self.check = jsonschema_gate.JsonSchemaGate('{p/builtin:jsonschema:list_of_string}')
        self.instruction_template = instruction_template
        self.tmpl = axiomic.Text(instruction_template)
        self.sysprompt = axiomic.Text(sysprompt_template)

    def infer(self, list_of_strings: list):
        serialized = json.dumps(list_of_strings)
        req = self.tmpl.format(criteria=self.criteria, list_of_strings=serialized)
        return self.check.infer(req.infer(system_prompt=self.sysprompt))
    
    def test_infer(self, w):
        pass
        

