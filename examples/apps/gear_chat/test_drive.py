

import sys

import utils


import gear_agents
import argparse

import axiomic
import axiomic.models as models




def get_text(text_or_none):
    if text_or_none:
        return text_or_none
    # read from stdin
    return sys.stdin.read()


def main():
    parser = argparse.ArgumentParser(description='Load agents from a directory.')
    subparsers = parser.add_subparsers(dest='agent_type', help='Agent type')

    # Gather Agent
    gather_parser = subparsers.add_parser('gather', help='Gather Agent')
    gather_parser.add_argument('dirname', type=str, help='Path to the directory containing agent definitions')
    gather_parser.add_argument('--text', type=str, help='Text to feed the agent')

    # Elect Agent
    elect_parser = subparsers.add_parser('elect', help='Elect Agent')
    elect_parser.add_argument('dirname', type=str, help='Path to the directory containing agent definitions')
    elect_parser.add_argument('text', type=str, help='Text to feed the agent')

    # Author Agent
    author_parser = subparsers.add_parser('author', help='Author Agent')
    author_parser.add_argument('dirname', type=str, help='Path to the directory containing agent definitions')
    author_parser.add_argument('text', type=str, help='Text to feed the agent')
    author_parser.add_argument('--instructions', type=str, help='instructions for the author agent', default='Remind the user to pass --instructions and ask again.')

    # Review Agent
    review_parser = subparsers.add_parser('review', help='Review Agent')
    review_parser.add_argument('dirname', type=str, help='Path to the directory containing agent definitions')
    review_parser.add_argument('text', type=str, help='Text to feed the agent')

    args = parser.parse_args()

    gather, elect, author, review = gear_agents.load_agents(args.dirname)
    if args.agent_type == 'gather':
        with models.Generic.Text.Large:
            print(gather.infer(get_text(args.text)))
    elif args.agent_type == 'elect':
        with models.Generic.Text.Small:
            print(elect.infer(get_text(args.text)))
    elif args.agent_type == 'author':
        print(author.infer(get_text(args.text), args.instructions))
    elif args.agent_type == 'review':
        print(review.infer(get_text(args.text)))


if __name__ == '__main__':
    main()
