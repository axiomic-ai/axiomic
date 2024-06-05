
from typing import List, Tuple

import axiomic.logalytics as logalytics

import dataclasses


@dataclasses.dataclass
class EmbeddingRequest:
    embedding_provider_name: str
    embedding_model_name: str
    text: str


@dataclasses.dataclass
class EmbeddingResponse:
    embedding_provider_name: str
    embedding_model_name: str
    embedding: list
    duration_s: float


class EmbeddingProvider:
    def __init__(self, impl):
        self.impl = impl

    def get_default_context_params(self):
        return self.impl.get_default_context_params()
    
    def get_provider_name(self):
        return self.impl.get_provider_name()

    def infer(self, req: EmbeddingRequest) -> EmbeddingRequest:
        # provider_name = llm_history_inference.llm_provider_name

        resp = self.impl.infer(req)
        return resp

        # info = {
        #     'model_name': llm_history_inference.model_name,
        #     'temperature': llm_history_inference.temperature,
        #     'max_tokens': llm_history_inference.max_tokens,
        #     'user_message': llm_history_inference.user_message,
        #     'system_prompt': llm_history_inference.system_prompt,
        #     'history_pairs': llm_history_inference.history_pairs
        # }

        #with logalytics.LlmInference(provider_name, info) as c:
        #    resp = self.llm_provider_ipml.infer_history(llm_history_inference)
        #    c.end(model_name=llm_history_inference.model_name, input_tokens=resp.input_tokens, output_tokens=resp.output_tokens, duration_s=resp.duration_s, response=resp.response)
        #    return resp

