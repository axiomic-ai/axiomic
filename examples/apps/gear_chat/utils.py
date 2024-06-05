import argparse
import os
import pydantic
import yaml
from typing import List
from enum import Enum
import dataclasses


import axiomic.data as data
import axiomic.data.lists as lists


GATHER_DEFINITION_FILE = 'gather_definition.yaml'
GATHER_EXAMPLES_FILE = 'gather_examples.yaml'
ELECT_DEFINIITON_FILE = 'elect_definition.yaml'
ELECT_EXAMPLES_FILE = 'elect_examples.yaml'
AUTHOR_DEFINITION_FILE = 'author_definition.yaml'
AUTHOR_EXAMPLES_FILE = 'author_examples.yaml'
REVIEW_DEFINITION_FILE = 'review_definition.yaml'
REVIEW_EXAMPLES_FILE = 'review_examples.yaml'
GATHER_ELECT_EVAL_FILE = 'elect_eval.yaml'


class GatherItemReq(pydantic.BaseModel):
    name: str
    description: str


class GatherReq(pydantic.BaseModel):
    text: str
    items: List[GatherItemReq]


class Gathered(Enum):
    NO_DATA = 'NO_DATA'
    PARTIAL = 'PARTIAL'
    COMPLETE = 'COMPLETE'


class GatherItemResp(pydantic.BaseModel):
    name: str
    extraction: str
    extracted: Gathered


class GatherResp(pydantic.BaseModel):
    items: List[GatherItemResp]


class GatherDefinition(pydantic.BaseModel):
    description: str
    items: List[GatherItemReq]


class ElectCase(pydantic.BaseModel):
    case_name: str
    criteria: str
    next_step: str


class ElectDefinition(pydantic.BaseModel):
    cases: List[ElectCase]


class AuthorDefinition(pydantic.BaseModel):
    author_instructions: str


class AuthorReq(pydantic.BaseModel):
    conversation: str
    reply_instructions: str


class AuthorResp(pydantic.BaseModel):
    reply: str


class ReviewReq(pydantic.BaseModel):
    conversation: str


class ReviewDefinition(pydantic.BaseModel):
    review_instructions: str


class ReviewResult(Enum):
    REVIEW_PASSED = 'REVIEW_PASSED'
    REVIEW_FAILED = 'REVIEW_FAILED'


class ReviewResp(pydantic.BaseModel):
    chain_of_thought: str
    review_result: ReviewResult


@dataclasses.dataclass
class GEARChatData:
    # Gather
    gather_examples: lists.ChatList
    gather_definition: GatherDefinition

    # Elect
    elect_examples: lists.ChatList
    elect_definition: ElectDefinition

    # Author
    author_examples: lists.ChatList
    author_definition: AuthorDefinition

    # Review
    review_examples: lists.ChatList
    review_definition: ReviewDefinition


def load_gather(dirname):
    gather_def_file = os.path.join(dirname, GATHER_DEFINITION_FILE)
    with open(gather_def_file, 'r') as f:
        yam = yaml.load(f, Loader=yaml.FullLoader)

    gather_exmaples_file = os.path.join(dirname, GATHER_EXAMPLES_FILE)
    gather_examples = data.load_chat_pydantic(gather_exmaples_file,
                                              user_model=GatherReq,
                                              agent_model=GatherResp)
    
    return gather_examples, GatherDefinition(**yam)


def load_elect(dirname):
    elect_def_filename = os.path.join(dirname, ELECT_DEFINIITON_FILE)
    with open(elect_def_filename, 'r') as f:
        yam = yaml.load(f, Loader=yaml.FullLoader)
    elect_def = ElectDefinition(**yam)
    elect_examples_filename = os.path.join(dirname, ELECT_EXAMPLES_FILE)
    elect_examples = data.load_chat_text(elect_examples_filename)
    return elect_examples, elect_def


def load_author(dirname):
    def_filename = os.path.join(dirname, AUTHOR_DEFINITION_FILE)
    exmaples_filename = os.path.join(dirname, AUTHOR_EXAMPLES_FILE)
    with open(def_filename, 'r') as f:
        yam = yaml.load(f, Loader=yaml.FullLoader)
    author_def = AuthorDefinition(**yam)
    author_examples = data.load_chat_pydantic(exmaples_filename, AuthorReq, AuthorResp)
    return author_examples, author_def


def load_review(dirname):
    review_examples = data.load_chat_pydantic(os.path.join(dirname, REVIEW_EXAMPLES_FILE), ReviewReq, ReviewResp)
    with open(os.path.join(dirname, REVIEW_DEFINITION_FILE), 'r') as f:
        yam = yaml.load(f, Loader=yaml.FullLoader)
    review_def = ReviewDefinition(**yam)
    return review_examples, review_def


def load_dir(dirname):
    gather_examples, gather_definition = load_gather(dirname)
    elect_examples, elect_definition = load_elect(dirname)
    author_examples, author_definition = load_author(dirname)
    review_examples, review_definition = load_review(dirname)

    return GEARChatData(
        gather_examples=gather_examples,
        gather_definition=gather_definition,
        elect_examples=elect_examples,
        elect_definition=elect_definition,
        author_examples=author_examples,
        author_definition=author_definition,
        review_examples=review_examples,
        review_definition=review_definition
    )


def load_elect_eval_examples(dirname):
    filename = os.path.join(dirname, GATHER_ELECT_EVAL_FILE)
    return data.load_chat_text(filename)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("dirname", help="Directory name")
    args = parser.parse_args()

    dirname = args.dirname
    gear_chat_data = load_dir(dirname)

    print("Gather Examples:", gear_chat_data.gather_examples)
    print("Gather Definition:", gear_chat_data.gather_definition)
    print("Elect Examples:", gear_chat_data.elect_examples)
    print("Elect Definition:", gear_chat_data.elect_definition)
    print("Author Examples:", gear_chat_data.author_examples)
    print("Author Definition:", gear_chat_data.author_definition)
    print("Review Examples:", gear_chat_data.review_examples)
    print("Review Definition:", gear_chat_data.review_definition)

if __name__ == "__main__":
    main()