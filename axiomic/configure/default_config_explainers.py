
import rich
import atexit
from rich import print
from rich.panel import Panel
from rich.text import Text
from rich.console import Group
from rich.traceback import install


'''
These explainers are separated from the rest because the main set of explainers
depends on the default configs.

These explainers have no deps within axiomic.
'''


ALMOST_THERE_WEAVE = Text("Almost there! There was a minor config uh oh.", style='bold yellow reverse', justify="center")
IF_NOT_YOUR_FAULT_REPORT = Text("If you believe this is an internal error, please file a github issue.", style='dim', justify="center")

AT_EXIT_EXPLAINERS = []

def exit_handler():
    if len(AT_EXIT_EXPLAINERS) == 0:
        return
    rich.print("\n")
    rich.print("\n")
    for explainer in AT_EXIT_EXPLAINERS:
        rich.print(explainer)
    rich.print()

atexit.register(exit_handler)


def explain_missing_path(name, file_path, examples_of_setting):
    title = "Path Not Found"
    l = [Text(e, style='dim', justify="left") for e in examples_of_setting]
    content = Group(
        Text(f"Please set or create {name}", style='dim', justify="center"),
        Text(f"\n{file_path}\n", style="red bold", justify="center"),
        Text(f"Consider one of the these...", style='dim', justify="left"),
        *l
    )

    explanation_panel = Panel(
        content,
        title=title,
        expand=False,
        border_style="bold yellow",
    )
    # AT_EXIT_EXPLAINERS.append(ALMOST_THERE_WEAVE)
    AT_EXIT_EXPLAINERS.append(explanation_panel)
    AT_EXIT_EXPLAINERS.append(IF_NOT_YOUR_FAULT_REPORT)
    raise ValueError(f'Missing {name}: {file_path}')

