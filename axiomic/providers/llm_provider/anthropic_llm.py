
import axiomic.providers.llm_provider.llm_provider as llm_provider

import anthropic
import time
import os

import axiomic.errors as errors


if "ANTHROPIC_API_KEY" in os.environ:
    client = anthropic.Anthropic(
        # defaults to os.environ.get("ANTHROPIC_API_KEY")
        # api_key="my_api_key",
    )
else:
    client = None


# best_model = "claude-3-opus-20240229"
# model_sonnet = 'claude-3-sonnet-20240229'


def complete_history(prompt, model_name, max_tokens, system=None, history_pairs=[]):
    extra = {}
    if system:
        extra['system'] = system

    messages = [ ]

    for user, agent in history_pairs:
        messages.append({"role": "user", "content": user})
        messages.append({"role": "assistant", "content": agent})

    messages.append({"role": "user", "content": prompt})

    start = time.time()
    message = client.messages.create(
        model=model_name,
        max_tokens=max_tokens,
        messages=messages,
        **extra
    )
    end = time.time()
    
    return message.content[0].text, message.usage.input_tokens, message.usage.output_tokens, end - start


class AntropicLlmProvider:

    def get_default_context_params(self):
        return {'llm_provider_name': 'anthropic_text', 'llm_model_name': 'claude-3-sonnet-20240229', 'llm_temperature': 0.5, 'llm_max_tokens': 1024}

    def get_provider_name(self):
        return 'anthropic_text'

    def infer_history(self, llm_history_inference: llm_provider.LlmHistoryInferenceRequest) -> llm_provider.LlmInferenceResponse:
        retriable_error_text = None
        try:
            response, in_toks, out_toks, dur_s = complete_history(llm_history_inference.user_message, 
                                                                llm_history_inference.model_name, 
                                                                llm_history_inference.max_tokens, 
                                                                history_pairs=llm_history_inference.history_pairs,
                                                                system=llm_history_inference.system_prompt)
        except anthropic.InternalServerError as e:
            retriable_error_text = str(e)
        except anthropic.RateLimitError as e:
            retriable_error_text = str(e)

        if retriable_error_text:
            raise errors.ProviderErrorRetriable(retriable_error_text)

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
