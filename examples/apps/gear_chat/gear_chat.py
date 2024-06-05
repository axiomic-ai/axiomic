import argparse

import utils
import gear_agents

import axiomic.data.lists as lists


from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
import axiomic.models as models



class GEARChat:
    def __init__(self, gear_dir):
        self.gear_dir = gear_dir
        self.chat_list = lists.ChatList()
        self.gather, self.elect, self.author, self.review = gear_agents.load_agents(self.gear_dir)

    def infer(self, user):
        conversation = self.chat_list.format(most_recent_user=user)

        # Gather, Elect, Author, Review
        gathered_info = self.gather.infer(conversation)
        print(gathered_info)
        elected_case, elected_next_step = self.elect.infer(gathered_info)
        authored_response = self.author.infer(conversation, elected_next_step)
        review_result = self.review.infer(authored_response)

        # Book keep and return
        review_ok = review_result == utils.ReviewResult.REVIEW_PASSED
        self.chat_list.append(user, authored_response)
        return review_ok, elected_case, authored_response
        

def _chat_inner_loop(console, gear_chat):
    while True:
        user = Prompt.ask("You")
        review_ok, elected_case, authored_response = gear_chat.infer(user)
        formatted_message = Panel(authored_response, title="Agent Case: " + elected_case, subtitle="Review: " + ("Passed" if review_ok else "Failed"), border_style="dim")
        console.print(formatted_message)


def chat_loop(gear_chat):
    console = Console()
    console.print("Use ^D to exit the chat.")

    try:
        _chat_inner_loop(console, gear_chat)
    except EOFError:
        console.print("Goodbye!")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('gear_dir', metavar='DIR', help='the directory name which defines the GEAR agents.')
    args = parser.parse_args()
    # Rest of your code goes here
    text = 'Hello, I need help with my computer.'
    gear_chat = GEARChat(args.gear_dir)
    with models.Generic.Text.Large:
       chat_loop(gear_chat)


if __name__ == '__main__':
    main()