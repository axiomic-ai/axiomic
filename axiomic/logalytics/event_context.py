import threading

import axiomic.logalytics.events as events

import axiomic.logalytics.sink as sink


class EventContextManager:
    _thread_local = threading.local()  # Thread-local storage

    def __init__(self, name, event_type: events.EventType, fields: dict):
        self.name = name
        self.event_type = event_type
        self.fields = fields
        self.event = events.Event(name, event_type, fields)
        self.closed = False

    def __enter__(self):
        if not hasattr(EventContextManager._thread_local, 'stack'):
            EventContextManager._thread_local.stack = []  # Initialize stack if not present
        EventContextManager._thread_local.stack.append(
            self)  # Push the current context onto the stack
        sink.event_sink(self.event)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Pop the current context from the stack
        if exc_val is not None:
            EventContextManager._thread_local.stack.pop()
            return 
        if self.event_type in events.MAP_START_TO_END.keys() and not self.closed:
            raise Exception('InternalError: Failed to close event')
        
        if self.event_type == events.EventType.TASK_START:
            event = events.Event(self.name, events.EventType.TASK_SUCCESS, self.fields)
            sink.event_sink(event)
        EventContextManager._thread_local.stack.pop()
    
    def end(self, **kwargs):
        self.closed = True
        end_type = events.MAP_START_TO_END[self.event_type]
        event = events.Event(self.name, end_type, kwargs)
        sink.event_sink(event)

    def task_fail(self, fields: dict):
        event = events.Event(self.name, events.EventType.TASK_FAILURE, fields)
        sink.event_sink(events.Event(event))



def Task(name, fields: dict):
    return EventContextManager(name, events.EventType.TASK_START, fields)


def LlmInference(name, fields: dict):
    return EventContextManager(name, events.EventType.LLM_INFERENCE_START, fields)

def ImageInference(name, fields: dict):
    return EventContextManager(name, events.EventType.IMAGE_INFERENCE_START, fields)

def RagQuery(name, fields: dict):
    return EventContextManager(name, events.EventType.RAG_QUERY_START, fields)


def _global_event_chain():
    if not hasattr(EventContextManager._thread_local, 'stack'):
        return []
    return EventContextManager._thread_local.stack



