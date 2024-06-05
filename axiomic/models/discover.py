
import inspect
import os

import axiomic.providers.default_providers as default_providers

import axiomic.models.context as _context

import axiomic.logalytics.sink as sink

import axiomic.models.models_openai as quick_openai
import axiomic.models.models_together as quick_together
import axiomic.models.models_anthropic as quick_anthropic
import axiomic.models.generic as generic
import axiomic.configure.runtime_config as runtime_config


Generic = generic.Generic


def discover_user_calling_file():
    frame = inspect.currentframe()
    weave_package_name = "axiomic" 

    while frame:
        module_name = frame.f_globals.get("__name__")
        if module_name and not module_name.startswith(weave_package_name):
            calling_file = frame.f_code.co_filename
            return os.path.abspath(calling_file)
        frame = frame.f_back
    return None


def _discovery(env_key, prov):
    if env_key not in os.environ:
        return
    _context.register_global_provider(prov)
    _context.GLOBAL_DEFAULT_CONTEXT.update_non_none(**prov.get_default_context_params())


def _announce_provider(env_key, models_name):
    if env_key in os.environ:
        sink.discover_config(f'discovered {env_key}, models available under models.{models_name}')


def discover_providers():
    _context.register_global_ref_provider(default_providers.FILESYSTME_PARAMS)

    _announce_provider('OPENAI_API_KEY', 'OpenAI')
    _announce_provider('ANTHROPIC_API_KEY', 'Anthropic')
    _announce_provider('TOGETHER_API_KEY', 'Together')

    # Open AI discovery
    _discovery('OPENAI_API_KEY', default_providers.OPENAI_LLM)
    _discovery('OPENAI_API_KEY', default_providers.OPENAI_IMG)
    _discovery('OPENAI_API_KEY', default_providers.OPENAI_EMBED)

    if 'OPENAI_API_KEY' in os.environ:
        quick_openai.OpenAI.bind()

    # Anthropic Discovery
    _discovery('ANTHROPIC_API_KEY', default_providers.ANTHROPIC_LLM)

    if 'ANTHROPIC_API_KEY' in os.environ:
        quick_anthropic.Anthropic.bind()

    # Together Discovery
    _discovery('TOGETHER_API_KEY', default_providers.TOGETHER_LLM)
    _discovery('TOGETHER_API_KEY', default_providers.TOGETHER_IMG)

    if 'TOGETHER_API_KEY' in os.environ:
        quick_together.Together.bind()
