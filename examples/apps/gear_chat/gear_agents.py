
import utils

import axiomic.core.uagents as uagents
import axiomic.core.modules as modules



def _format_gather(gather_resp):
    s = ''
    for item in gather_resp.items:
        s += f'{item.name}: [{item.extracted}] {item.extraction}\n'
    return s


class GatherAgent:
    
    def __init__(self, gather_def: utils.GatherDefinition, gather_examples):
        self.gather_definition = gather_def
        self.gather_examples = gather_examples
        self.extract_items = gather_def.items
        self.pattern = uagents.PydanticPattern(self.gather_examples, self.gather_definition.description)

    def infer(self, text):
        req = utils.GatherReq(text=text, items=self.extract_items)
        return _format_gather(self.pattern.infer(req))


def quote_if_not_quoted(s):
    if s[0] == '"' and s[-1] == '"':
        return s
    return f'"{s}"'


def build_elect_description(elect_def):
    desc = 'You need to choose which case applies best to the information you are given'
    for case in elect_def.cases:
        desc += f'\n{case.case_name}: {case.criteria}'
    
    return desc


class ElectAgent:
    def __init__(self, elect_examples, elect_def):
        self.elect_def = elect_def
        self.examples = [(e.user, quote_if_not_quoted(e.agent)) for e in elect_examples]
        self.instructions = build_elect_description(elect_def)
        self.switch = modules.Switch(self.examples, instructions=self.instructions)
        self.case_name_to_next_step = {case.case_name: case.next_step for case in self.elect_def.cases}

    def infer(self, text):
        case_name = self.switch.infer(text).value_json()
        return case_name, self.case_name_to_next_step[case_name]

    def get_case_names(self):
        return self.case_name_to_next_step.keys()


class ReviewAgent:

    def __init__(self, review_examples, review_def):
        self.review_def = review_def
        self.examples = review_examples
        self.pattern = uagents.PydanticPattern(self.examples, self.review_def.review_instructions)

    def infer(self, text):
        return self.pattern.infer(text).review_result


class AuthorAgent:
    
    def __init__(self, author_examples, author_def):
        self.author_def = author_def
        self.examples = author_examples
        self.pattern = uagents.PydanticPattern(self.examples, self.author_def.author_instructions)

    def infer(self, conversation, reply_instructions):
        req = utils.AuthorReq(conversation=conversation, reply_instructions=reply_instructions)
        return self.pattern.infer(req).reply


def load_agents(dirname):
    defs = utils.load_dir(dirname)
    gather = GatherAgent(defs.gather_definition, defs.gather_examples)
    elect = ElectAgent(defs.elect_examples, defs.elect_definition)
    author = AuthorAgent(defs.author_examples, defs.author_definition)
    review = ReviewAgent(defs.review_examples, defs.review_definition)

    return gather, elect, author, review
