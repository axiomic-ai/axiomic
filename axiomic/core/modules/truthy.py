
import axiomic.configure as configure

import axiomic.core.modules.chat as chat
import axiomic.core.checks as checks

import axiomic.data.lists as lists
import axiomic


class Truthy:
    
    def __init__(self, instructions=None):
        if instructions is None:
            self.instructions = '{P.core.modules.truthy.instructions}'
        else:
            self.instructions = instructions
        self.system_prompt = axiomic.Text('{P.core.modules.truthy.system_prompt_template}').format(instructions=self.instructions)
        self.check = checks.CheckJsonSchema('{P.core.jsonschema.boolean}')

    def infer(self, testable_text):
        testable_text = axiomic.Text(testable_text)
        answer = axiomic.infer(testable_text, system_prompt=self.system_prompt)
        return answer.checkpoint(checks.CheckJsonSyntax())
