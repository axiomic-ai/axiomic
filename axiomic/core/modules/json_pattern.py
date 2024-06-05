import axiomic.configure as configure

import axiomic.core.modules.chat as chat
import axiomic.core.checks as checks

import axiomic.data.lists as lists

import yaml
import axiomic


class JsonPattern:
    '''
    Have the agent continue a pattern genering a JSON response (i.e. few shot prompting).

    .. code-block:: python

        import axiomic.core.modules as modules
        examples = [('Jack and Jill', '[{"name": "Jack"}, {"name": "Jill"}]')]   
        examples.append(('Jake out ran Mark", [{"name": "Jake"}, {"name": "Mark"}]'))
        json_schema = '{ "type": "array", "items": { "type": "object", "properties": { "name": { "type": "string" } }, "required": ["name"] } }'
        pattern = modules.JsonPattern(examples, json_schema)

        resp = pattern.infer('The 1967 film Bonnie and Clyde is directed by Arthur Penn')
        assert resp.unweave_json() == [{"name": "Bonnie"}, {"name": "Clyde"}, {"name": "Arthur Penn"}]

    Args:
        chat_list: A few examples of user-agent interactions to extrapolate from.
        json_schema: A JSON schema that the response must match.
        pattern_desc: (optional) A description of the pattern.
        system_prompt_template: (optional) Defaults to `'{P.builtin.knits.json_pattern_system_prompt}'`. Only recommended to set this if the default isn't working or you want to save tokens.
        append_mode: Defaults to false, but will keep adding each new response as a new few shot example, eventually becoming many shot.

    This pattern preseves the graph - it does not unaxiomic.
    '''
    def __init__(self, chat_list: lists.ChatListType, 
                 json_schema: axiomic.TextType, 
                 pattern_desc: axiomic.TextType = 'Continue the pattern', 
                 system_prompt_template: axiomic.TextType = None,
                 append_mode=False):
        self.chat_list = lists.ChatList(chat_list)
        self.pattern_desc = pattern_desc
        self.append_mode = append_mode
        if system_prompt_template is None:
            system_prompt_template = '{P.core.knits.json_pattern.system_prompt}'
        self.system_prompt_template = system_prompt_template
        self.system_prompt = axiomic.format(system_prompt_template, pattern_desc=pattern_desc, schema=json_schema)
        self.json_schema = json_schema
        self.json_schema_checked = axiomic.Text(json_schema).checkpoint(checks.CheckJsonSyntax())
        self.check_json_schema = checks.CheckJsonSchema(self.json_schema)
        self.chat = chat.Chat(chat_list=self.chat_list, system_prompt=self.system_prompt, append_mode=append_mode)

    def infer(self, prompt, name=None):
        '''
        Infers the next response in the pattern.

        Args:
            prompt: The user prompt.

        Returns:
            The agent response as a Weave, checked against the JSON schema.
        '''
        w = axiomic.Text(prompt)
        resp = self.chat.infer(w, name=name).checkpoint(checks.CheckJsonSyntax()).checkpoint(self.check_json_schema)
        return resp

