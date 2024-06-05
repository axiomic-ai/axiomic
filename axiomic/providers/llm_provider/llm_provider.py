
from typing import List, Tuple

import axiomic.logalytics as logalytics

import dataclasses


@dataclasses.dataclass
class LlmHistoryInferenceRequest:
    llm_provider_name: str
    model_name: str
    temperature: float
    max_tokens: int
    user_message: str
    system_prompt: str
    history_pairs: List[Tuple[str, str]]


@dataclasses.dataclass
class LlmInferenceResponse:
    llm_provider_name: str
    model_name: str
    temperature: float
    max_tokens: int
    response: str
    input_tokens: int
    output_tokens: int
    duration_s: float


class LlmProvider:
    def __init__(self, llm_provider_ipml):
        self.llm_provider_ipml = llm_provider_ipml

    def get_default_context_params(self):
        return self.llm_provider_ipml.get_default_context_params()
    
    def get_provider_name(self):
        return self.llm_provider_ipml.get_provider_name()

    def infer_history(self, llm_history_inference: LlmHistoryInferenceRequest) -> LlmInferenceResponse:
        provider_name = llm_history_inference.llm_provider_name

        info = {
            'model_name': llm_history_inference.model_name,
            'temperature': llm_history_inference.temperature,
            'max_tokens': llm_history_inference.max_tokens,
            'user_message': llm_history_inference.user_message,
            'system_prompt': llm_history_inference.system_prompt,
            'history_pairs': llm_history_inference.history_pairs,
            'provider_name': provider_name
        }

        with logalytics.LlmInference(provider_name, info) as c:
            resp = self.llm_provider_ipml.infer_history(llm_history_inference)
            c.end(model_name=llm_history_inference.model_name, input_tokens=resp.input_tokens, output_tokens=resp.output_tokens, duration_s=resp.duration_s, response=resp.response, provider_name=provider_name)
            return resp
