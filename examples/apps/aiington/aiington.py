import argparse
import axiomic as ax
import sys

import axiomic.core.modules as modules
import axiomic.configure as configure
import axiomic.data.loaders as loaders

ax.models.set_relative_data_root('./weave_data')
ROUTES = loaders.load_chat_text('$WEAVE_DATA_ROOT/data/routes.yaml')

for r in ROUTES:
    print(r)

router = modules.Switch(ROUTES)
    
def route_user_input(user_input):
    return router.infer(user_input)

GENERAL_SYS_PROMPT = '{P.aidams_char_sysprompt}'

def hanlde_critisim(user_input):
    return ax.format('{P.general_critism_response}', user_input=user_input, system_prompt=GENERAL_SYS_PROMPT).infer()

def handle_friendly(user_input):
    return ax.format('{P.general_friendly_response}', user_input=user_input, system_prompt=GENERAL_SYS_PROMPT).infer()

def handle_other(user_input):
    return ax.format('{P.general_other_response}', user_input=user_input, system_prompt=GENERAL_SYS_PROMPT).infer()

def make_a_declaration(user_input):
    return ax.format('{P.make_a_declaration}', user_input=user_input, system_prompt=GENERAL_SYS_PROMPT).infer()


HANDLERS = {
    'REPLY_CRITISIM': hanlde_critisim,
    'REPLY_FRIENDLY': handle_friendly,
    'REPLY_DECLARATION': make_a_declaration,
    # ROUTE_OTHER: handle_other
}


def route_to_handler(user_input, n=1):
    with ax.models.Generic.Text.Medium:
        route = route_user_input(user_input)
        raw_route = route.value_json()
        print('Route: ', raw_route)
    options = [HANDLERS[raw_route](user_input) for _ in range(n)]
    return options


def main():
    parser = argparse.ArgumentParser(description='Process user input.')
    parser.add_argument('--prompt', type=str, default=None, help='User input to be processed.')
    args = parser.parse_args()
    prompt = args.prompt
    if args.prompt is None:
        print()
        print('Enter something to reply to (then ^D):')
        prompt = sys.stdin.read()
    with ax.models.Generic.Text.Large:
        options = route_to_handler(prompt, n=1)
    for o in options:
        print()
        print(o.value())
        print()

if __name__ == '__main__':
    main()