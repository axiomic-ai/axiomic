
import axiomic.configure as configure

import axiomic.core.modules.chat as chat

import axiomic.core.modules.json_pattern as json_pattern 

import yaml
import axiomic

import axiomic.data.lists as lists
import json
import pydantic


def pydantic_to_str(pydantic_obj):
    if not isinstance(pydantic_obj, pydantic.BaseModel):
        return pydantic_obj
    
    return pydantic_obj.json()


class PydanticPattern:
    '''
    Continues a given pattern which produces Pydnatic objects (i.e. few shot prompting).

    .. code-block:: python

        import axiomic.builtins.uagents as uagents
        import pydantic
                
        class COTAnswer(pydantic.BaseModel):
            rationale: str
            answer: bool

        EXAMPLES = [
            ('a car is bigger than an apple.', COTAnswer(rationale='In general, cars weight more than apples', answer=True)),
            ('A tree is smaller than a pencile', COTAnswer(rationale='in general, penciles are made of part of a tree, so a tree cannot be smaller', answer=False)),
        ]

        pattern = pydantic_pattern.PydanticPattern(EXAMPLES, 'Explain your thinking then evalute the statements as true or false')
        assert pattern.infer('dogs are bigger than cats').answer == True

    Args:
        examples: A few examples of user-agent interactions to extrapolate from. The user message must be a string. The agent message must be pydnatic object.
        pattern_desc: A description of the pattern.
        system_prompt_template: (optional) Defaults to a reasonable template. Only recommended to set this if the default isn't working or you want to save tokens.

    This is a micro agent - it will `unweave()` when creating the response.
    '''
    def __init__(self, examples: lists.ChatListType, pattern_desc: axiomic.TextType, system_prompt_template: axiomic.TextType = None):
        self.chat_list = lists.ChatList(examples)
        self.pattern_desc = pattern_desc
        if len(examples) == 0:
            raise ValueError('examples must be non-empty')
        self.examples = examples
        self.json_schema = json.dumps(examples[0][1].model_json_schema())
        self.serialized_examples = lists.ChatList([(pydantic_to_str(e[0]), e[1].json()) for e in examples])
        self.json_pattern = json_pattern.JsonPattern(chat_list=self.serialized_examples, 
                                                     json_schema=self.json_schema, 
                                                     pattern_desc=pattern_desc, 
                                                     system_prompt_template=system_prompt_template)
        self.ModelClass = self.examples[0][1].__class__

    def infer(self, prompt, name=None):
        '''
        Returns the pydantic object that matches the pattern for `prompt`.

        Since this returns a pydnatic object, it will `unweave()` the response and the graph won't be propogated.

        Args:
            prompt: The next prompt in the pattern.

        Returns:
            The agent response as a Pydantic object.
        '''
        resp = self.json_pattern.infer(pydantic_to_str(prompt), name=name)
        j = resp.value_json()
        return self.ModelClass(**j)
