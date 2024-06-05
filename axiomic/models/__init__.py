import os

import axiomic.configure.default_config as default_config
import axiomic.models.discover as discover
import axiomic.models.context as context


# These are exported to users

from axiomic.models.generic import Generic, bind

from axiomic.models.models_together import Together
from axiomic.models.models_openai import OpenAI
from axiomic.models.models_anthropic import Anthropic


discover.discover_providers()

Config = context.Config
'''
Create a new config, for exmaple,

    .. code-block:: python

        import axiomic.models
        GPT3_5 = axiomic.models.Config(
            llm_provider_name='openai_text',
            llm_model_name='gpt-3.5-turbo',
            llm_temperature=0.5,
            llm_max_tokens=1024,
            _context_name='OpenAiGpt3_5'
        )

        with GP3_5:
            axiomic.infer('What is the meaning of life?').print()

'''


VerboseText = context.Config(verbose_llm=True, _context_name='VerboseText')
'''
Makes text inference verbose. For example;

    .. code-block:: python
        import axiomic.models
        with axiomic.models.VerboseText:
            response = axiomic.infer('How much wood would a woodchuck chuck?', system_prompt='Respond in only 1 sentence.').value()

'''

MaxTokens32 = context.LLMConfig(llm_max_tokens=32, _context_name='MaxTokens32')
''' Sets Max Output Tokens to 128 '''

MaxTokens64 = context.LLMConfig(llm_max_tokens=64, _context_name='MaxTokens64')
''' Sets Max Output Tokens to 128 '''

MaxTokens128 = context.LLMConfig(llm_max_tokens=128, _context_name='MaxTokens128')
''' Sets Max Output Tokens to 128 '''

MaxTokens256 = context.LLMConfig(llm_max_tokens=256, _context_name='MaxTokens256')
"""Sets Max Output Tokens to 256"""

MaxTokens512 = context.LLMConfig(llm_max_tokens=512, _context_name='MaxTokens512')
"""Sets Max Output Tokens to 512"""

MaxTokens1024 = context.LLMConfig(llm_max_tokens=1024, _context_name='MaxTokens1024')
"""Sets Max Output Tokens to 1024"""

MaxTokens2048 = context.LLMConfig(llm_max_tokens=2048, _context_name='MaxTokens2048')
"""Sets Max Output Tokens to 2048"""

MaxTokens4096 = context.LLMConfig(llm_max_tokens=4096, _context_name='MaxTokens4096')
"""Sets Max Output Tokens to 4096"""

MaxTokens8192 = context.LLMConfig(llm_max_tokens=8192, _context_name='MaxTokens8192')
"""Sets Max Output Tokens to 8192"""


Temperature0_0 = context.LLMConfig(llm_temperature=0.0, _context_name='Temperature0_0')
''' Sets LLM temperature to 0.0 '''

Temperature0_1 = context.LLMConfig(llm_temperature=0.1, _context_name='Temperature0_1')
''' Sets LLM temperature to 0.1 '''

Temperature0_2 = context.LLMConfig(llm_temperature=0.2, _context_name='Temperature0_2')
''' Sets LLM temperature to 0.2 '''

Temperature0_3 = context.LLMConfig(llm_temperature=0.3, _context_name='Temperature0_3')
''' Sets LLM temperature to 0.3 '''

Temperature0_4 = context.LLMConfig(llm_temperature=0.4, _context_name='Temperature0_4')
''' Sets LLM temperature to 0.4 '''

Temperature0_5 = context.LLMConfig(llm_temperature=0.5, _context_name='Temperature0_5')
''' Sets LLM temperature to 0.5 '''

Temperature0_6 = context.LLMConfig(llm_temperature=0.6, _context_name='Temperature0_6')
''' Sets LLM temperature to 0.6 '''

Temperature0_7 = context.LLMConfig(llm_temperature=0.7, _context_name='Temperature0_7')
''' Sets LLM temperature to 0.7 '''

Temperature0_8 = context.LLMConfig(llm_temperature=0.8, _context_name='Temperature0_8')
''' Sets LLM temperature to 0.8 '''

Temperature0_9 = context.LLMConfig(llm_temperature=0.9, _context_name='Temperature0_9')
''' Sets LLM temperature to 0.9 '''

Temperature1_0 = context.LLMConfig(llm_temperature=1.0, _context_name='Temperature1_0')
''' Sets LLM temperature to 1.0 '''


def global_default(model_config):
    '''
    Updates the global default context. For example,

    .. code-block:: python

        import axiomic.models as models
        models.global_default(models.Generic.Text.Large)
        models.global_default(models.Temperature0_7)
        models.global_default(models.MaxTokens2048)

    '''
    context.GLOBAL_DEFAULT_CONTEXT.update_from(model_config.context)
    
def infer_context():
    '''
    Returns the current context.

    For example,

    .. code-block:: python

        import axiomic.models as models
        with models.SmallText & models.MaxTokens256 & models.Temperature0_5:
            print(models.infer_context())

    '''
    return context.infer_context()

def print_context():
    '''
    Prints the current context to the console.

    For example,
    
    .. code-block:: python

        import axiomic.configure.quick as wc
        with wc.SmallText & wc.MaxTokens256 & wc.Temperature0_5:
            wc.print_context()

    '''
    context.print_inferred_context()


def get_weave_data_root():
    if default_config.file_ref_store.data_path is None:
        return ''
    return default_config.file_ref_store.data_path


def set_relative_data_root(relative_path: str):
    """
    Sets the relative path to the weave data root directory.

    Args:
        relative_path (str): The relative path to the weave data root directory.
    """
    user_filename = discover.discover_user_calling_file()
    user_dirname = os.path.dirname(user_filename)
    weave_path = os.path.join(user_dirname, relative_path)
    default_config.file_ref_store.data_path = weave_path


def resolve_axiomic_variables(text):
    """
    Resolves weave variables in the text.

    Args:
        text (str): The text to resolve variables in.

    Returns:
        str: The text with variables resolved.
    """
    replaces = {
        '$WEAVE_DATA_ROOT': get_weave_data_root()
    }

    for key, value in replaces.items():
        text = text.replace(key, value)
    
    return text


def get_provider_provider():
    '''
    Returns the provider provider.

    For example,

    .. code-block:: python

        import axiomic.models as models
        models.get_provider_provider()

    '''
    return context.get_provider_provider()