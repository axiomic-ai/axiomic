
from rich import print
from rich.status import Status
from contextlib import contextmanager

from rich.console import Console, Group
from rich.panel import Panel
from rich.text import Text
from rich import box
from rich.layout import Layout


import axiomic.logalytics.events as events
import axiomic.configure as configure
import axiomic.configure.default_config as default_config
# import axiomic.models as models


@contextmanager
def spinner(message="Processing...", spinner="aesthetic"):
    status = Status(message, spinner=spinner)
    status.start()
    try:
        yield
    finally:
        status.stop()

def start_spinner(message="Processing..."):
    global spinner_context
    spinner_context = spinner(message=message)
    spinner_context.__enter__()

def stop_spinner():
    spinner_context.__exit__(None, None, None)


def verbose_llm_inference_end(e: events.Event):
    # 'model_name', 'duration_s', 'input_tokens', 'output_tokens', 'response'
    model_name = e.info.model_name
    duration_s = e.info.duration_s
    input_tokens = e.info.input_tokens
    output_tokens = e.info.output_tokens
    response = e.info.response
    console = Console()

    footer_text = Text(f"Model: {model_name} | Duration: {duration_s:.2f}s | Input Tokens: {input_tokens} | Output Tokens: {output_tokens}", style="bold")

    # Main panel that includes the layout and footer
    main_panel = Panel(response, title="LLM Inference - Response", style='green', subtitle=footer_text, box=box.ROUNDED, expand=True)

    # Print the main panel
    console.print(main_panel)

    

def verbose_llm_inference(e: events.Event):
    model_name = e.info.model_name
    history_pairs = e.info.history_pairs
    temperature = e.info.temperature
    max_tokens = e.info.max_tokens
    user_message = e.info.user_message
    system_prompt = e.info.system_prompt

    console = Console()

    panel_list = []
    # Create a sub-panel for the system prompt
    if system_prompt:
        panel_list.append(Panel(system_prompt, title="System Prompt")) #, expand=False))

    for i, pair in enumerate(history_pairs):
        panel_list.append(Panel(pair[0], style="dim", title=f"History #{i} - User"))
        panel_list.append(Panel(pair[1], style="dim", title=f"History #{i} - Assistant"))
    # Create sub-panels for history pairs
    # history_panels = [Panel(pair, expand=False) for pair in history_pairs]

    # Create a sub-panel for the user message
    panel_list.append(Panel(user_message, title="User Prompt"))

    # Layout to hold all sub-panels

    panel_group = Group(*panel_list)

    # Footer information as a Text object
    footer_text = Text(f"Model: {model_name} | Temperature: {temperature} | Max Tokens: {max_tokens}", style="bold")
    
    # Main panel that includes the layout and footer
    main_panel = Panel(panel_group, title="LLM Inference - Request", style='dark_green', subtitle=footer_text, box=box.ROUNDED, expand=True)

    # Print the main panel
    console.print(main_panel)


class ConsoleLog:
    def __init__(self):
        pass

    def log_event(self, event: events.Event):
        if event.event_type == events.EventType.LLM_INFERENCE_END:
            self.log_llm_inference_end(event)
        elif event.event_type == events.EventType.LLM_INFERENCE_START:
            self.log_llm_inference_start(event)
        elif event.event_type == events.EventType.RAG_QUERY_START:
            self.rag_query_start(event)
        elif event.event_type == events.EventType.RAG_QUERY_END:
            self.rag_query_end(event)
        elif event.event_type == events.EventType.CONFIG_DISCOVER:
            self.config_discover(event)
        elif event.event_type == events.EventType.IMAGE_INFERENCE_START:
            self.log_image_inference_start(event)
        elif event.event_type == events.EventType.IMAGE_INFERENCE_END:
            self.log_image_inference_end(event)
        else:
            print(f'{event.name} :: {event.info}')

    def log_image_inference_start(self, event: events.Event):
        start_spinner(message=f'Image Inference: {event.name} {event.info.image_model_name} -> {event.info.image_width}x{event.info.image_height}')

    def log_image_inference_end(self, event: events.Event):
        stop_spinner()
        print(f'[bold][blue]{event.name}: {event.info.image_model_name} -> {event.info.image_width}x{event.info.image_height} (in {event.info.duration_s:.2f}s)[/blue][/bold]')

    def config_discover(self, event: events.Event):
        print(f'[dim](axiomic) {event.info.message}[/dim]')

    def log_llm_inference_start(self, event: events.Event):
        # print(f'{event.name} :: {event.info.model_name}')
        # if models.infer_context().verbose_llm:
        #    verbose_llm_inference(event)
        start_spinner(message=f'LLM Inference: {event.name} {event.info.model_name}')

    def log_llm_inference_end(self, event: events.Event):
        stop_spinner()
        print(f'[bold][blue]{event.name}: {event.info.input_tokens} toks -> {event.info.model_name} -> {event.info.output_tokens} toks (in {event.info.duration_s:.2f}s)[/blue][/bold]')
        # if configure.infer_context().verbose_llm:
        #    verbose_llm_inference_end(event)

    def rag_query_start(self, event: events.Event):
        start_spinner(message=f'RAG: {event.info.rag_provider} k={event.info.k}')
    
    def rag_query_end(self, event: events.Event):
        stop_spinner()
        print(f'[bold][dark_green]RAG: {event.info.rag_provider} k={event.info.k} -> {len(event.info.results)} results (in {event.info.duration_s:.2f}s)[/bold][/dark_green]')

