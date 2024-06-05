
import collections
from typing import List
from typing import List, Tuple, Union

import pydantic

from rich import print
from rich.panel import Panel
from rich.columns import Columns
from rich.syntax import Syntax
from rich.json import JSON
from rich.console import Console
from rich.layout import Layout
from rich.console import Group
from rich.text import Text

console = Console()

ChatPair = collections.namedtuple('ChatPair', ['user', 'agent'])

class TextList:
    
    def __init__(self, strings: any = [], name: str = None):
        if isinstance(strings, TextList):
            self.strings = strings.strings
        elif isinstance(strings, list):
            self.strings = strings
        self.name = name
        self.strigns = strings

    def __len__(self):
        return len(self.strings)

    def __getitem__(self, index):
        return self.strings[index]

    def __iter__(self):
        return iter(self.strings)

    def print(self):
        _print_list(self)



TextListType = Union[TextList, List[any]]


class ChatList:
    def __init__(self, pairs: any = None, name: str = None):
        self.name = name
        if pairs is None:
            self.pairs = []
        elif isinstance(pairs, ChatList):
            self.pairs = pairs.pairs
        else:
            # TODO add more type checking before assuming it is a list of tuples
            self.pairs = [ChatPair(user, agent) for user, agent in pairs]

    def __len__(self):
        return len(self.pairs)

    def __getitem__(self, index):
        return self.pairs[index]

    def __iter__(self):
        return iter(self.pairs)

    def append(self, user, agent):
        self.pairs.append(ChatPair(user, agent))

    def as_list(self):
        return [(pair.user, pair.agent) for pair in self.pairs]

    def extend(self, pairs):
        self.pairs.extend(ChatList(pairs).pairs)

    def copy(self):
        return ChatList(list(self.pairs))

    def make_eval_varients(self):
        varients = []
        for i in range(len(self.pairs)):
            cur = self.pairs[i]
            all_others = self.pairs[:i] + self.pairs[i+1:]
            varients.append((cur, ChatList(all_others, self.name)))
        return varients

    def print(self):
        _print_chat(self)

    def format(self, user_title="user", agent_title="agent", major_delim="\n============\n", minor_delim="\n---------\n", most_recent_user=None):
        txt = major_delim.join([f"{user_title}: {pair.user}{minor_delim}{agent_title}: {pair.agent}" for pair in self.pairs])

        if most_recent_user is not None:
            txt += f"{major_delim}{user_title}: {most_recent_user}"

        return txt


def _convert_for_print(thing):
    if isinstance(thing, str):
        return thing, 'string' #Syntax(thing, "json")
    if isinstance(thing, pydantic.BaseModel):
        o = JSON(thing.json())
        return o, f"pydantic<{type(thing).__name__}>"
    return JSON(thing), 'json'


def _print_chat(chat_list: ChatList):
    # Create a list of panel groups
    def create(c, idx):
        u, u_footer = _convert_for_print(c.user)
        a, a_footer = _convert_for_print(c.agent)
        panel_u = Panel(u, title="User" + str(idx), width=int(console.width // 2) - 2, subtitle=u_footer)
        panel_a = Panel(a, title="Agent" + str(idx), width=int(console.width // 2) - 2, subtitle=a_footer)
        return Columns([
            panel_u, panel_a
        ], expand=True )
    panel_groups = [ create(c, i) for i, c in enumerate(chat_list) ]
    # Display each group of panels
    for group in panel_groups:
        print(group)


def _print_list(wlist: TextList):
    # Create a list of panel groups
    def create(c, idx):
            item, footer = _convert_for_print(c)
            return Panel(item, title="Item " + str(idx), width=int(console.width) - 2, subtitle=footer)
    panel_groups = [ create(c, i) for i, c in enumerate(wlist) ]
    # Display each group of panels
    for group in panel_groups:
        print(group)


ChatListType = Union[ChatList, List[Tuple[any, any]]]

if __name__ == '__main__':
    print(str(ChatList([('a', 'b'), ('c', 'd')]).pairs))