
import axiomic.errors as errors
import axiomic

import rich

import atexit
import os
import json


'''
def bad_name_explainer(name):
    """
    Given a bad name, return an explanation of why it is bad.
    """
'''

from rich import print
from rich.panel import Panel
from rich.text import Text
from rich.console import Group
import axiomic.errors as errors
import sys

import axiomic.configure.default_config as default_config

from rich.traceback import install


if default_config.console_config.enable:
    rich.print("[dim](axiomic) weave in helpful console mode (export AXIOMIC_CONSOLE_ENABLE=False to disable).[/dim]")

if default_config.console_config.enable and default_config.console_config.color_tracebacks:
    install(show_locals=False) #, suppress=[weave, json])

OLD_SYS_EXCEPT_HOOK = sys.excepthook

def thought_crime_exception_handler(exc_type, exc_value, exc_traceback):
    if exc_type is errors.ThoughtCrime:
        dying_to_thoughtcrime(exc_value)
    OLD_SYS_EXCEPT_HOOK(exc_type, exc_value, exc_traceback)


RAN_ONCE = {}

def only_once(f):
    def wrapped(*args, **kwargs):
        if f in RAN_ONCE:
            return
        RAN_ONCE[f] = True
        return f(*args, **kwargs)
    return wrapped


# Set the custom exception handler
sys.excepthook = thought_crime_exception_handler

ALMOST_THERE_WEAVE = Text("Axiomic: Almost there! A minor issue with the weave was found.", style='bold yellow reverse', justify="center")

THOUGHT_CRIME_BANNER = Text("Axiomic: Exit due to uncaught Thoguht Crime.", style='bold red reverse', justify="center")

IF_NOT_YOUR_FAULT_REPORT = Text("If you believe this is an internal error, please file a github issue.", style='dim', justify="center")

FOR_GRUMPY = Text("""export AXIOMIC_CONSOLE_COLOR_TRACEBACKS=False; export AXIOMIC_CONSOLE_HELP_ON_EXIT=False; # if you'd prefer a simpler experience.""", style='dim', justify="left")

AT_EXIT_EXPLAINERS = []

def exit_handler():
    if len(AT_EXIT_EXPLAINERS) == 0:
        return
    rich.print(FOR_GRUMPY)
    rich.print()
    for explainer in AT_EXIT_EXPLAINERS:
        rich.print(explainer)
    rich.print()

if default_config.console_config.enable and default_config.console_config.help_on_exit:
    atexit.register(exit_handler)


def explain_missing_file(file_path):
    title = "File Needs Creation"
    content = Group(
        Text("Please create this file.", style='dim', justify="center"),
        Text(f"\n{file_path}\n", style="red bold", justify="center"),
    )

    explanation_panel = Panel(
        content,
        title=title,
        expand=False,
        border_style="bold yellow",
    )
    AT_EXIT_EXPLAINERS.append(ALMOST_THERE_WEAVE)
    AT_EXIT_EXPLAINERS.append(explanation_panel)
    AT_EXIT_EXPLAINERS.append(IF_NOT_YOUR_FAULT_REPORT)
    raise errors.GraphError(text=f'Missing File: {file_path}')

def explain_wrapped_name(bad_name):
    title = "Invalid Name"

    content = Group(
        Text("Name incorrectly wrapped in '{' '}'   ", style='dim', justify="center"),
        Text(f"\nName: {bad_name}\n", style="red bold", justify="center"),
        Text("Try removing the { } around the name.", style='dim', justify="center"),
        Text("This name is not being used in a subsitution.", style='dim', justify="center"),
    )

    explanation_panel = Panel(
        content,
        title=title,
        # expand=False,
        border_style="bold yellow",
        # justify="center",
    )

    g = Group(ALMOST_THERE_WEAVE, explanation_panel, IF_NOT_YOUR_FAULT_REPORT)
    # AT_EXIT_EXPLAINERS.append(ALMOST_THERE_WEAVE)
    # AT_EXIT_EXPLAINERS.append(explanation_panel)
    # AT_EXIT_EXPLAINERS.append(IF_NOT_YOUR_FAULT_REPORT)
    AT_EXIT_EXPLAINERS.append(g)
    raise errors.GraphError(text=f'Bad Name: {bad_name}')

def explain_bad_name_error(bad_name):
    title = "Invalid Name"

    content = Group(
        Text("Name does not match [BUCKET:][DIR:]BASENAME   ", style='dim', justify="center"),
        Text(f"\nName: {bad_name}\n", style="red bold", justify="center"),
        Text("(optional) BUCKET    ~ [a-zA-Z][a-zA-Z0-9_.-]+", style='dim', justify="center"),
        Text("(optional) DIR       ~ [a-zA-Z][a-zA-Z0-9_.-]+", style='dim', justify="center"),
        Text("           BASENAME  ~ [a-zA-Z][a-zA-Z0-9_.-]+", style='dim', justify="center"),
        Text("Example: code_gen_prompt", style='dim', justify="center"),
        Text("Example: prompts:chat_prompts:friendly_hello", style='dim', justify="center"),
    )

    explanation_panel = Panel(
        content,
        title=title,
        # expand=False,
        border_style="bold yellow",
        # justify="center",
    )

    g = Group(ALMOST_THERE_WEAVE, explanation_panel, IF_NOT_YOUR_FAULT_REPORT)
    # AT_EXIT_EXPLAINERS.append(ALMOST_THERE_WEAVE)
    # AT_EXIT_EXPLAINERS.append(explanation_panel)
    # AT_EXIT_EXPLAINERS.append(IF_NOT_YOUR_FAULT_REPORT)
    AT_EXIT_EXPLAINERS.append(g)
    raise errors.GraphError(text=f'Bad Name: {bad_name}')


def missing_file_ref(file_ref, file_path):
    title = "File Ref Not Found"

    content = Group(
        Text("Looking for this ref", style='dim', justify="center"),
        Text(f"\n{file_ref}\n", style="red bold", justify="center"),
        Text("Leads to this fle", style='dim', justify="center"),
        Text(f"\n{file_path}\n", style="red bold", justify="center"),
        Text("Consider creating the file or changing the ref name. ", style='dim', justify="left"),
        Text(f"mkdir -p {os.path.dirname(file_path)} ", style='dim', justify="left"),
        Text(f"touch {file_path} ", style='dim', justify="left"),
    )

    explanation_panel = Panel(
        content,
        title=title,
        # expand=False,
        border_style="bold yellow",
        # justify="center",
    )

    g = Group(ALMOST_THERE_WEAVE, explanation_panel, IF_NOT_YOUR_FAULT_REPORT)
    # AT_EXIT_EXPLAINERS.append(ALMOST_THERE_WEAVE)
    # AT_EXIT_EXPLAINERS.append(explanation_panel)
    # AT_EXIT_EXPLAINERS.append(IF_NOT_YOUR_FAULT_REPORT)
    AT_EXIT_EXPLAINERS.append(g)
    raise errors.GraphError(text=f'Missing File Reference: {file_ref}')


@only_once
def set_file_store_path():
    title = "Set File Store Path"

    content = Group(
        Text("Please set the file store path, for example...", style='dim', justify="center"),

        Text('mkdir -p ./my_weave_data', style='dim', justify="left"),
        Text('THEN', style='dim', justify="center"),
        Text("import axiomic.configure.quick as quick", style='dim', justify="left"),
        Text('quick.set_relative_weave_data_root("./weave_data")', style='dim', justify="left"),
        Text('OR', style='dim', justify="center"),
        Text("export WEAVE_FILE_DATA_PATH=./my_weave_data", style='dim', justify="left"),
    )

    explanation_panel = Panel(
        content,
        title=title,
        # expand=False,
        border_style="bold yellow",
        # justify="center",
    )

    g = Group(ALMOST_THERE_WEAVE, explanation_panel, IF_NOT_YOUR_FAULT_REPORT)
    # AT_EXIT_EXPLAINERS.append(ALMOST_THERE_WEAVE)
    # AT_EXIT_EXPLAINERS.append(explanation_panel)
    # AT_EXIT_EXPLAINERS.append(IF_NOT_YOUR_FAULT_REPORT)
    AT_EXIT_EXPLAINERS.append(g)
    raise errors.GraphError(text=f'File Store Path Not Set')

def dying_to_thoughtcrime(tc):
    title = "axiomic.errors.ThoughtCrime"

    content = Group(
        Text(str(tc), style='dim', justify="left"),
    )

    explanation_panel = Panel(
        content,
        title=title,
        border_style="bold red",
    )

    g = Group(THOUGHT_CRIME_BANNER, explanation_panel, IF_NOT_YOUR_FAULT_REPORT)
    AT_EXIT_EXPLAINERS.append(g)

# Example usage
#bad_name = "invalid_name!"
#explain_bad_name_error(bad_name)

# explain_missing_file("/Users/victor/repos/weave/weave/logalytics/events.py")

