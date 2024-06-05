

import axiomic.providers.llm_provider.llm_provider as llm_provider

from together import Together
import time
import os

API_KEY = os.environ.get("TOGETHER_API_KEY", None)

if API_KEY:
    client = Together(api_key=os.environ.get("TOGETHER_API_KEY"))
else:
    client = None


def complete_history(prompt, model_name, max_tokens, system=None, history_pairs=[]):
    messages = [ ]

    if system:
        messages.append({"role": "system", "content": system})

    for user, agent in history_pairs:
        messages.append({"role": "user", "content": user})
        messages.append({"role": "assistant", "content": agent})

    messages.append({"role": "user", "content": prompt})

    start = time.time()

    response = client.chat.completions.create(
        model=model_name,
        messages=messages,
        max_tokens=max_tokens,
    )

    end = time.time()
    return response.choices[0].message.content, response.usage.prompt_tokens, response.usage.completion_tokens, end - start


class TogetherProviderLlmImpl:

    def get_default_context_params(self):
        return {'llm_provider_name': 'together_text', 'llm_model_name': 'meta-llama/Llama-3-8b-chat-hf', 'llm_temperature': 0.5, 'llm_max_tokens': 1024}

    def get_provider_name(self):
        return 'together_text'

    def infer_history(self, llm_history_inference: llm_provider.LlmHistoryInferenceRequest) -> llm_provider.LlmInferenceResponse:
        response, in_toks, out_toks, dur_s = complete_history(llm_history_inference.user_message, 
                                                            llm_history_inference.model_name, 
                                                            llm_history_inference.max_tokens, 
                                                            history_pairs=llm_history_inference.history_pairs,
                                                            system=llm_history_inference.system_prompt)

        resp = llm_provider.LlmInferenceResponse(
            llm_provider_name=llm_history_inference.llm_provider_name,
            model_name=llm_history_inference.model_name,
            temperature=llm_history_inference.temperature,
            max_tokens=llm_history_inference.max_tokens,
            response=response,
            input_tokens=in_toks,
            output_tokens=out_toks,
            duration_s=dur_s
        )
            
        return resp
    


