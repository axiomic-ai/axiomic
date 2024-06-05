import threading

import axiomic.providers.provider as provider

import axiomic.configure.default_config as default_config

import rich
from rich.console import Console, Group
from rich.panel import Panel
from rich.text import Text
from rich import box
from rich.layout import Layout


from icecream import ic

'''
TODO: This file needs major cleanup.
'''

class ModelContext:
    def __init__(self, name=None):
        self.provider_provider = None
        self.llm_provider_name = None
        self.llm_model_name = None
        self.llm_temperature = None
        self.llm_max_tokens = None
        self.verbose_llm = None
        self._context_name = name
        self.image_provider_name = None
        self.image_model_name = None
        self.image_width = None
        self.image_height = None
        self.embedding_provider_name = None
        self.embedding_model_name = None
    
    def __str__(self):
        return str(self.__dict__)

    def bless_as_global(self):
        '''Does anything that needs to be done once for the global context.
        '''
        self.provider_provider = provider.ProviderProvider()

    def update_non_none(self, **kwargs):
        for k, v in kwargs.items():
            if v is not None:
                setattr(self, k, v)

    def update_all(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
    
    def update_from(self, other, preserve_name=True):
        items = other.__dict__.copy()
        if preserve_name:
            del items['_context_name']
        self.update_non_none(**items)

    def __and__(self, other):
        neu = self.clone()
        neu.update_non_none(**other.__dict__)
        neu._context_name = f'{self._context_name} & {other._context_name}'
        return neu

    def clone(self):
        '''
        Clones the ModelContext.
        '''
        new_context = ModelContext()
        new_context.update_all(**self.__dict__)
        return new_context

    def __repr__(self):
        d = self.__dict__.copy()
        # filter out Nones
        d = {k: v for k, v in d.items() if v is not None}

        stuff = str(d)
        return f'ModelContext({stuff})'


class ContextStack:
    def __init__(self, root_config):
        self.stack = [root_config]

    def push_context(self, context):
        self.stack.append(context)
    
    def pop_context(self):
        if len(self.stack) == 1:
            raise Exception('Cannot pop the root context.')
        self.stack.pop()

    def get(self, name):
        stack = self.stack
        for c in reversed(self.stack):
            if hasattr(c, name) and getattr(c, name) is not None:
                return getattr(c, name)
        raise Exception(f'Could not resolve config name: {name}')

    def __getattr__(self, name):
        return self.get(name)


class ModelContextManager:
    _thread_local = threading.local()  # Thread-local storage

    def __init__(self, context: ModelContext):
        if isinstance(context, ContextStack):
            raise Exception('Should not be a context stack.')
        self.context = context
        if not hasattr(ModelContextManager._thread_local, 'current'):
            ModelContextManager._thread_local.current = ContextStack(GLOBAL_DEFAULT_CONTEXT)

    def __str__(self):
        return str(self.context.__dict__)

    def __enter__(self):
        if not hasattr(ModelContextManager._thread_local, 'current'):
            ModelContextManager._thread_local.current = ContextStack(GLOBAL_DEFAULT_CONTEXT)
        current = ModelContextManager._thread_local.current
        current.push_context(self.context)  # Set current context for this thread
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        current = ModelContextManager._thread_local.current
        current.pop_context()  # Clear current context for this thread

    def __and__(self, other):
        return ModelContextManager(self.context & other.context)

    def __repr__(self):
        return f'ModelContextManager(context={repr(self.context)}'


GLOBAL_DEFAULT_CONTEXT = ModelContext(name='Global Context')
GLOBAL_DEFAULT_CONTEXT.verbose_llm = default_config.llm_config.verbose
GLOBAL_DEFAULT_CONTEXT.bless_as_global()


def Config(_context_name=None, **kwargs):
    '''
    Context Manager which will set the values in the config.
    '''
    neu = ModelContext(name=_context_name)
    neu.update_all(**kwargs)
    return ModelContextManager(neu)


def LLMConfig(llm_provider_name: str = None, llm_model_name: str = None, llm_temperature: float = None, llm_max_tokens: int = None, _context_name=None):
    '''
    Creates an LLMSet context.
    '''
    if _context_name is None:
        _context_name = 'LLMConfig'
    return Config(llm_provider_name=llm_provider_name, llm_model_name=llm_model_name, llm_temperature=llm_temperature, llm_max_tokens=llm_max_tokens, _context_name=_context_name)


def infer_context():
    '''
    Attempts to determine the current ModelContext which applies to the caller.
    Returns None if it was unable to.
    '''
    possible_context = getattr(ModelContextManager._thread_local, 'current', None)
    if possible_context is not None:
        return possible_context
    return global_default_context()

def _context_to_panel(title, c):
    txt = ''
    for k, v in c.__dict__.items():
        if k == '_context_name':
            continue
        if k == 'provider_provider':
            continue
        if v is None:
            continue
        txt += f'{k}: {v}\n'
    txt = txt.strip()
    p = Panel(txt, title=title, style='dim')
    return p
    

def print_inferred_context():
    '''Pretty prints the inferred context.
    '''
    context = infer_context()
    
    if context == global_default_context():

        panel = _context_to_panel('GlobalContext', context) 
        # print('Global Default Context:', context)
    else:
        panels = []
        for i, c in enumerate(context.stack):
            context_name = c._context_name
            if context_name is None:
                context_name = f'(Anonymous Context)'
            panels.append(_context_to_panel(context_name, c))
        panel = Group(*panels)
        # print('Context Stack:', context.stack)
    context_stack = Panel(panel, title='Context Stack', style='dim', expand=True)
    console = Console()
    console.print(context_stack)
    


def global_default_context():
    return GLOBAL_DEFAULT_CONTEXT

def register_global_provider(provider):
    '''
    Registers a provider in the global context.
    '''
    return global_default_context().provider_provider.register_provider(provider)
    

def register_global_ref_provider(ref_provider):
    '''
    Registers a provider in the global context.
    '''
    global_default_context().provider_provider.ref_store_provider = ref_provider
    

def get_provider_provider():
    return infer_context().provider_provider
    