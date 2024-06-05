
import yaml
import axiomic
import axiomic.configure as configure

import axiomic.data.lists as lists

class Chat:
    '''
    A basic chat where the user says something and the agent responds.

    .. code-block:: python

        import axiomic.core.modules as modules
        chat = modules.Chat(system_prompt='Speak like a pirate')
        chat.infer('Hello! My favorite color is blue!').print()
        chat.infer('What is my favorite color?').print()

    By default, it will keep a conversation history. If you do not want a history to be
    kept, and want to do few shot prompting, you can set `append_mode=False`.

    This chat preseves the graph - it does not unaxiomic.

    Create a new chat.

    Args:
        chat_list: A list of chat pairs to start with. Default is no history.
        system_prompt: A prompt to use for how the agent should act over the conversation. Default is no specific system prompt.
        append_mode: If True, the chat will keep a history of the conversation from one call to `.infer()` to the next. If False, the only history will be `chat_pairs`.
    '''
    def __init__(self, chat_list: lists.ChatListType = None, 
                 system_prompt: axiomic.TextType = None, 
                 append_mode: bool = True):
        self.history = lists.ChatList(chat_list)
        self.system_prompt = system_prompt
        self.new_chats = lists.ChatList()
        self.append_mode = append_mode

    def get_history(self):
        '''
        Format the chat history as a string.
        '''
        return lists.ChatList(self.history.pairs + [(c.user.value(),  c.agent.value()) for c in self.new_chats.pairs])

    def set_system_prompt(self, system_prompt):
        '''
        Change the system prompt.
        
        Args:
            system_prompt: A prompt to use for how the agent should act over the conversation.
        '''
        self.system_prompt = system_prompt

    def set_append_mode(self, append_mode):
        '''
        Change if history is being kept.

        Args: 
            append_mode: If True, the chat will keep a history of the conversation from one call to `.infer()` to the next. If False, the only history will be `chat_pairs`.
        '''
        self.append_mode = append_mode

    def add_chat(self, user, agent):
        '''
        Inject a chat pair into the history as the most recent chat.

        Args:
            user: What the user said.
            agent: What the agent said.
        '''
        self.new_chats.append(user, agent)

    def add_chats(self, chat_list: lists.ChatListType):
        '''
        Add a list of chat pairs to the history as the the most recent chats.

        Args:
            chat_list: A list of chat pairs to add to the history.
        '''
        self.history.extend(chat_list)

    def infer(self, user, name=None):
        '''
        Send a user message to the the agent and get a response.

        If `append_mode` is True, the chat history will be updated with the new chat pair.

        Args:
            user: What the user said.
            name: A name to use for the Weave response. Default is unnamed (None).

        Returns:
            A weave which represents the agent's response.
        '''
        w = axiomic.Text(user)
        full_history = self.history.copy()
        full_history.extend(self.new_chats)
        resp = w.infer(system_prompt=self.system_prompt, history_pairs=full_history, name=name)
        if self.append_mode:
            self.add_chat(w, resp)
        return resp
