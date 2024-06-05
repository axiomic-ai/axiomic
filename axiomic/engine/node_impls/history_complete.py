
import axiomic.protos as protos

import axiomic.providers.llm_provider.llm_provider as llm_provider
import axiomic.models as models

import re
import json

from icecream import ic 

import axiomic.configure.runtime_config as runtime_config

ic.configureOutput(includeContext=True)


def history_complete(node: protos.axiomic.HistoryCompleteNode, c, weave_node: protos.axiomic.AxiomicNode) -> str:
    cw = c.resolve_node(node.user_message)
    history_pairs = []

    for pair in node.chat_history:
        user_message = c.resolve_node(pair.user_message)
        agent_message = c.resolve_node(pair.assistant_message)
        history_pairs.append((user_message, agent_message))
    sp = c.resolve_node(node.system_prompt)

    params = node.complete_params

    llm_provider_name = params.llm_provider_name
    llm_model_name = params.llm_model_name
    if 'RUNTIME:' in llm_provider_name:
        llm_provider_name, llm_model_name = runtime_config.resolve_runtime_provider_and_model(llm_provider_name, llm_model_name)

    req = llm_provider.LlmHistoryInferenceRequest(
        llm_provider_name,
        llm_model_name,
        params.llm_temperature,
        params.llm_max_tokens,
        cw,
        sp,
        history_pairs
    )

    resp = models.get_provider_provider().get_provider(llm_provider_name).infer_history(req)


    # print('history_copmlete.py: ask_history: Inferring for ', weave_node.name, '  ::: ', node.user_message.name, 'with complexity', complexity, 'system prompt', node.system_prompt.name)
    # resp = ask_history(cw, history_pairs, sp, complexity_level=complexity)
    return resp.response
