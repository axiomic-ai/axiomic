

from collections import namedtuple
from enum import Enum
import time


class EventType(Enum):
    TASK_START = 1
    TASK_SUCCESS = 2
    TASK_FAILURE = 3
    THOUGHT_CRIME = 4
    LLM_INFERENCE_START = 5
    LLM_INFERENCE_END = 6
    RAG_QUERY_START = 7
    RAG_QUERY_END = 8
    CONFIG_DISCOVER = 9
    IMAGE_INFERENCE_START = 10
    IMAGE_INFERENCE_END = 11
    THOUGHT_CRIME_RETRY = 12
    PARAM_THUMBS_DOWN = 13
    PARAM_THUMBS_UP = 14
    PARAM_PARTICIPATION = 15
    PARAM_THOUGHT_CRIME = 16


MAP_START_TO_END = {
    EventType.LLM_INFERENCE_START: EventType.LLM_INFERENCE_END,
    EventType.RAG_QUERY_START: EventType.RAG_QUERY_END,
    EventType.IMAGE_INFERENCE_START: EventType.IMAGE_INFERENCE_END
}


EVENTS = {
    EventType.LLM_INFERENCE_START: namedtuple('LlmInferenceStart', ['model_name', 'temperature', 'max_tokens', 'user_message', 'system_prompt', 'history_pairs', 'provider_name']),
    EventType.LLM_INFERENCE_END: namedtuple('LlmInferenceEnd', ['model_name', 'duration_s', 'input_tokens', 'output_tokens', 'response', 'provider_name']),
    EventType.RAG_QUERY_START: namedtuple('RagQueryStart', ['query', 'k', 'rag_provider']),
    EventType.RAG_QUERY_END: namedtuple('RagQueryEnd', ['duration_s', 'k', 'results', 'rag_provider']),
    EventType.CONFIG_DISCOVER: namedtuple('ConfigDiscover', ['message']),
    EventType.IMAGE_INFERENCE_START: namedtuple('ImageInferenceStart', ['image_prompt', 'image_model_name', 'image_width', 'image_height', 'num_images', 'provider_name']),
    EventType.IMAGE_INFERENCE_END: namedtuple('ImageInferenceEnd', ['image_model_name', 'duration_s', 'image_list', 'image_width', 'image_height', 'provider_name']),
    EventType.THOUGHT_CRIME: namedtuple('ThoughtCrime', ['message']),
    EventType.THOUGHT_CRIME_RETRY: namedtuple('ThoughtCrimeRetry', ['message']),

    # Param Logalytics
    EventType.PARAM_THUMBS_DOWN: namedtuple('ParamThumbsDown', ['param_ref', 'param_ref_versioned']),
    EventType.PARAM_THUMBS_UP: namedtuple('ParamThumbsUp', ['param_ref', 'param_ref_versioned']),
    EventType.PARAM_THOUGHT_CRIME: namedtuple('ParamThoughtCrime', ['param_ref', 'param_ref_versioned'])
}


class Event:
    def __init__(self, name: str, event_type: EventType, fields: dict):
        self.name = name
        self.event_time = time.time()
        self.event_type = event_type
        self.info = EVENTS[event_type](**fields)
