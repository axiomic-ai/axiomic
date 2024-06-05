
import axiomic.configure as configure

import axiomic.core.modules.chat as chat
import axiomic.data.lists as lists

import yaml
import axiomic



class Pattern:
    def __init__(self, chat_list, system_prompt=None):
        self.chat_list = lists.ChatList(chat_list)
        self.chat_list.print()
        self.chat = chat.Chat(chat_list=self.chat_list, system_prompt=system_prompt, append_mode=False)
        

    def infer(self, next_a, name=None):
        w = axiomic.Text(next_a)
        return self.chat.infer(w, name=name)
