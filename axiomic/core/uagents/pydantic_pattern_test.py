
import pydantic

import axiomic.core.uagents.pydantic_pattern as pydantic_pattern


class COTTest(pydantic.BaseModel):
    rationale: str
    answer: bool


EXAMPLES = [
    ('a car is bigger than an apple.', COTTest(rationale='In general, cars weight more than apples', answer=True)),
    ('A tree is smaller than a pencile', COTTest(rationale='in general, penciles are made of part of a tree, so a tree cannot be smaller', answer=False)),
]


def test_basic():
    pat = pydantic_pattern.PydanticPattern(EXAMPLES, 'Explain your thinking then evalute the statements as true or false')
    assert pat.infer('dogs are bigger than cats').answer == True
    assert pat.infer('a mountain is weighs less than a person').answer == False