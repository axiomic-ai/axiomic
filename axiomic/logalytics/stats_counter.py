import rich
from rich.console import Console
from rich.table import Table


import axiomic.logalytics.events as events


class StatsCounter:
    def __init__(self):
        # Model -> (Count, Duration_s, Input Tokens, Output Tokens)
        self.models = {}

    def print_stats(self):
        if len(self.models) == 0:
            #rich.print()
            #rich.print('[dim]No LLM Inferences[/dim]')
            return

        console = Console()

        table = Table(show_header=True, header_style="dim", box=None)
        table.add_column("Provider", style="dim")
        table.add_column("Model", style="dim")
        table.add_column("Type", justify="right", style="dim")
        table.add_column("Reqs", justify="right", style="dim")
        table.add_column("Time (s)", justify="right", style="dim")
        table.add_column("Tok In", justify="right", style="dim")
        table.add_column("Tok Out", justify="right", style="dim")
        table.add_column("Out/s", justify="right", style="dim")

        rows = []
        for model in sorted(self.models.keys()):
            count, duration, input_tokens, output_tokens, provider_name = self.models[model]
            rate = '-'
            type_ = 'text'
            if duration > 0 and output_tokens > 0:
                rate = f'{output_tokens / duration:.2f}'
            elif duration > 0 and count > 0:
                rate = f'{count / duration:.2f}'
            if input_tokens < 0:
                input_tokens = '-'
                type_ = 'image'
            if output_tokens < 0:
                output_tokens = '-'
            rows.append((provider_name, model, type_, str(count), f'{duration:.2f}', str(input_tokens), str(output_tokens), f'{rate}'))
        
        for row in sorted(rows, key=lambda x: (x[1], x[0])):
            table.add_row(*row)
            

        console.print("\n")
        console.print(table)

    def record_image_inference(self, event: events.Event):
        if event.info.image_model_name not in self.models:
            self.models[event.info.image_model_name] = [0, 0, 0, 0, '']
        
        self.models[event.info.image_model_name][0] += 1
        self.models[event.info.image_model_name][1] += event.info.duration_s
        self.models[event.info.image_model_name][2] = -1
        self.models[event.info.image_model_name][3] = -1
        self.models[event.info.image_model_name][4] = event.info.provider_name

    def log_event(self, event: events.Event):
        if event.event_type == events.EventType.IMAGE_INFERENCE_END:
            self.record_image_inference(event)
            return
        if event.event_type != events.EventType.LLM_INFERENCE_END:
            return
        
        if event.info.model_name not in self.models:
            self.models[event.info.model_name] = [0, 0, 0, 0, '']

        self.models[event.info.model_name][0] += 1
        self.models[event.info.model_name][1] += event.info.duration_s
        self.models[event.info.model_name][2] += event.info.input_tokens
        self.models[event.info.model_name][3] += event.info.output_tokens
        self.models[event.info.model_name][4] = event.info.provider_name
