

import axiomic.configure.runtime_config as runtime_config
import axiomic.models.context as context
import os

import axiomic.logalytics.sink as sink

Config = context.Config

class Generic:

    class Text:
            
        Small = Config(
            llm_provider_name='RUNTIME:small_text_provider',
            llm_model_name='RUNTIME:small_text_model',
            llm_temperature=0.5,
            llm_max_tokens=1024,
            _context_name='Generic.Text.Small'
        )
        ''' The default small LLM, e.g. Claude Haiku, which will be discovered based on env varibles and available API keys.  '''

        Medium = Config(
            llm_provider_name='RUNTIME:medium_text_provider',
            llm_model_name='RUNTIME:medium_text_model',
            llm_temperature=0.5,
            llm_max_tokens=1024,
            _context_name='Generic.Text.Medium'
        )
        ''' The default Medium LLM, e.g. GPT-3, Claude Sonnet, which will be discovered based on env varibles and available API keys.  '''

        Large = Config(
            llm_provider_name='RUNTIME:large_text_provider',
            llm_model_name='RUNTIME:large_text_model',
            llm_temperature=0.5,
            llm_max_tokens=1024,
            _context_name='Generic.Text.Large'
        )
        ''' The default Medium LLM, e.g. GPT-4, Claude Opus, which will be discovered based on env varibles and available API keys.  '''

    class Image:

        Medium = Config(
            image_provider_name='RUNTIME:medium_image_provider',
            image_model_name='RUNTIME:medium_image_model',
            image_width='RUNTIME:medium_image_width',
            image_height='RUNTIME:medium_image_height',
            _context_name='Generic.Image.Medium',
        )


def bind(generic_cfg, non_generic_cfg):
    '''
    Binds the generic configuration to a specific configuration.

    For exmaple,

    .. code-block:: python

        bind(Generic.Text.Small, quick_together.Together.Text.Llama.llama_3_70b_chat_hf)
    
    '''
    generic_cfg = generic_cfg.context
    non_generic_cfg = non_generic_cfg.context

    def maybe_set_attr(generic_cfg, non_generic_cfg, attr):
        if type(getattr(generic_cfg, attr)) != str:
            return

        if 'RUNTIME:' not in getattr(generic_cfg, attr):
            return

        runtime_attr_name = getattr(generic_cfg, attr).split(':')[-1]
        runtime_config.GLBOAL_RUNTIME_CONFIG.__setattr__(f'{runtime_attr_name}', getattr(non_generic_cfg, attr))

    for attr in dir(generic_cfg):
        if not attr.startswith('_'):
            maybe_set_attr(generic_cfg, non_generic_cfg, attr)

    # sink.discover_config(f'bind {generic_cfg._context_name} -> {non_generic_cfg._context_name}')


def bind_if_env_key(env_key, generic_cfg, non_generic_cfg):
    '''
    Binds the generic configuration to a specific configuration if the environment key is present.

    For exmaple,

    .. code-block:: python

        bind_if_env_key('TOGETHER_API_KEY', Generic.Text.Small, quick_together.Together.Text.Llama.llama_3_70b_chat_hf)
    
    '''
    if env_key in os.environ:
        bind(generic_cfg, non_generic_cfg)



class Binder:
    def __init__(self, env_key, bind_pairs):
        self.env_key = env_key
        self.bind_pairs = bind_pairs

    def has_env_key(self):
        return self.env_key in os.environ

    def bind(self):
        for generic_cfg, non_generic_cfg in self.bind_pairs:
            bind(generic_cfg, non_generic_cfg)
