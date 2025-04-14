
import axiomic.providers.llm_provider.llm_provider as llm_provider

import time
from google import genai
from google.genai import types
import os

API_KEY = os.environ.get("GOOGLE_API_KEY", None)

if API_KEY:
    client = genai.Client(api_key=API_KEY)
else:
    client = None

def complete_history(prompt, model_name, max_tokens, system=None, history_pairs=[]):
    messages = [ ]

    for user, agent in history_pairs:
        messages.append(
            types.UserContent(
                parts=[types.Part.from_text(text=user)]
            )
        )
        messages.append(
            types.ModelContent(
                parts=[types.Part.from_text(text=agent)]
            )
        )
    messages.append(
        types.UserContent(
            parts=[types.Part.from_text(text=prompt)]
        )
    )
    if system:
        config = types.GenerateContentConfig(
            max_output_tokens=max_tokens,
            system_instruction=system,
            # temperature=0.1
        )
    else:
        config = types.GenerateContentConfig(
            max_output_tokens=max_tokens,
            # temperature=0.1
        )

    start = time.time()
    response = client.models.generate_content(
        model=model_name,
        contents=messages,
        config=config
        )
    end = time.time()

    return response.text, response.usage_metadata.prompt_token_count, response.usage_metadata.candidates_token_count, end - start

class GoogleLlmProvider:
    def get_default_context_params(self):
        return {'llm_provider_name': 'google_text', 'llm_model_name': 'gemini-2.0-flash', 'llm_temperature': 0.5, 'llm_max_tokens': 1024}

    def get_provider_name(self):
        return 'google_text'

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
    



