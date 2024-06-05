import inspect
import json
import os
import rich
import rich.panel as rich_panel
import yaml

import axiomic.configure as configure
import axiomic.engine as engine
import axiomic.engine.functional as nF
import axiomic.errors as errors
import axiomic.protos as protos
import axiomic.utils.naming as naming

import axiomic.providers.embedding_provider.embedding_provider as embedding_provider

import axiomic.frontend.expand as expand
import axiomic.frontend.image as image
import axiomic.frontend.embedding as embedding

import axiomic.models as models

import axiomic.utils.wjson as wjson
import typing

import axiomic.data.lists as lists


DEFAULT_CONTEXT = None

class VarContext:
    def __init__(self, contents):
        self.name = contents['name']
        self.default = contents['default']


class ParamContext:
    def __init__(self, contents):
        self.name = contents['name']
        self.default = contents['default']


def handle_missing_param_file(param_name, filepath):
    raise errors.GraphError(f'Param file for \'{param_name}\' not found: {filepath}')


class TextContext:
    def __init__(self):
        self.base_dir = './weave_context'
        self._vars = {}
        self._params = {}

    def var_filename(self, var_name):
        return f'{self.base_dir}/{var_name}.var.yaml'

    def param_filename(self, param_name):
        p = f'{self.base_dir}/{param_name}.param.yaml'
        return os.path.abspath(p)

    def _load_var(self, var_name):
        with open(self.var_filename(var_name), 'r') as f:
            v = yaml.safe_load(f)
        self._vars[var_name] = VarContext(v)

    def load_param(self, param_name):
        if not os.path.exists(self.param_filename(param_name)):
            handle_missing_param_file(param_name, self.param_filename(param_name))

        with open(self.param_filename(param_name), 'r') as f:
            v = yaml.safe_load(f)
        self._params[param_name] = ParamContext(v)
        
    def var(self, var_name):
        v = self._vars.get(var_name)
        return Text(v.default, name=var_name)

    def param(self, param_name):
        if param_name not in self._params:
            self.load_param(param_name)

        p = self._params.get(param_name)
        return Text(p.default, name=param_name)



def _get_caller_info(levels_up=1):
    """
    Returns the filename and line number of the caller up N levels in the call stack.
    
    Args:
    levels_up (int): Number of levels up in the stack from the current function to find the caller.
    
    Returns:
    tuple: A tuple containing the filename and line number of the caller.
    """
    try:
        frame = inspect.currentframe()
        for _ in range(levels_up + 1):  # +1 to skip the current function's frame
            frame = frame.f_back
            if frame is None:
                return None, None  # No caller at this level
        return frame.f_code.co_filename, frame.f_lineno
    finally:
        del frame  # Prevent reference cycles


# Prints a nice string
def pretty_print_box(title, contents, levels_up=1, nav_breadcrumbs={}):
    for nav_key in nav_breadcrumbs:
        rich.print(f'[grey50]{nav_breadcrumbs[nav_key]} ({nav_key})[/grey50]')
    panel = rich_panel.Panel(contents, title=title, expand=False, title_align="left", border_style="grey50", style="grey50")
    rich.print(panel)


def default_context():
    global DEFAULT_CONTEXT
    if DEFAULT_CONTEXT is None:
        DEFAULT_CONTEXT = TextContext()
    return DEFAULT_CONTEXT


def var(name: str):
    return default_context().var(name)


def param(name: str):
    return default_context().param(name)


def recursive_imbed_refs(text: str) -> str:
    imbed_refs = naming.get_imbedded_refs(text)

    if len(imbed_refs) == 0:
        return text

    ref_provider = configure.infer_context().provider_provider.ref_store_provider
    for ref in imbed_refs:
        exact_substr = '{' + ref + '}'
        ref_value = ref_provider.get_default_value(ref)

        ref_value_recur = recursive_imbed_refs(ref_value)
        text = text.replace(exact_substr, ref_value_recur)
    
    return text

def ref(ref_name):
    name = naming.Name(ref_name)
    ref_provider = configure.infer_context().provider_provider.ref_store_provider
    ref_value = ref_provider.get_default_value(ref_name)
    nav_breadcrumbs = (ref_provider.get_ref_nav_breadcrumbs(ref_name))
    return Text(ref_value, name=name.original_name, nav_breadcrumbs=nav_breadcrumbs)


class Text:
    def __init__(self, node: any, eager=False, json=False, name=None, nav_breadcrumbs={}, autoexpand=True):
        self.eager = eager
        self.nav_breadcrumbs = nav_breadcrumbs
        self._value = None
        self.graph_builder = nF.GraphBuilder()
        self.given_name = name
        if isinstance(node, Text):
            self._clone_from(node)
        elif isinstance(node, protos.axiomic.AxiomicNode):
            self.node = node
            self.graph_builder.add_node(self.node)
            if name is not None:
                if name != node.name:
                    raise NotImplementedError('Name passing not supported yet')
        elif not isinstance(node, str):
            raise errors.GraphError(f'Must be a string: {node}')
        elif autoexpand and expand.text_needs_expand(node):
            expanded_into_weave = expand.recur_build_wave_with_subs(node, Text)
            self._clone_from(expanded_into_weave)
        else:
            self.node = nF.weave(self.graph_builder, node, name=name)
            self.graph_builder.add_node(self.node)
        expand.track_text(self)

    def __format__(self, format_spec):
        return expand.text_format_place_holder(self)

    def _clone_from(self, w):
        self.node = w.node
        self.eager = w.eager
        # TODO should this be a deep copy?
        self.graph_builder = w.graph_builder

    def _merger(self):
        m = Merger(eager=self.eager)
        m.merge_from(self)
        return m

    def infer_image(self, n=1, name=None):
        m = self._merger()
        c = models.infer_context()
        params = protos.axiomic.TextToImagesParams(
            image_provider_name=c.image_provider_name, 
            model_name=c.image_model_name, 
            image_width=c.image_width, 
            image_height=c.image_height, 
            num_images=n
        )
        img_infer_node = nF.infer_image(self.graph_builder, 
                                      self.node, 
                                      params=params,
                                      name=name)
        wi = image.Image(img_infer_node, eager=self.eager, name=name)
        m.merge_into(wi)
        return wi

    def print(self, verbose=True):
        '''
        Prints the resolved value of this Text to the console.
        This is not considered to value as it does not return the value to you.

        It will force resolution of this weave, and any associated LLM inferences which haven't bene completed yet.
        Therefore, it may raise any errors associated with `value()`, including a ThoughtCrime.
        
        Raises:
            ThoughtCrime: If there was an error building this weave by the AI.
            GraphError: If there was an error building this weave by the developer.
        '''
        name = self.given_name
        if name is None:
            name = ''
        else:
            name = f' - {name}'

        nav_breadcrumbs = {}
        if verbose:
            nav_breadcrumbs = dict(self.nav_breadcrumbs)
            filename, line_number = _get_caller_info(1)
            nav_breadcrumbs['printed'] = f'{filename}:{line_number}'
        
        pretty_print_box(f'Text{name}', self._unsafe_access(), nav_breadcrumbs=nav_breadcrumbs)
        return self

    def infer(self, system_prompt=None, history_pairs: lists.ChatListType = None, name=None):
        '''
        Does LLM text compleition on this weave, returning a Text which represents the completed text.

        The model used for completion is determined by the context, for example,

        .. code-block:: python

            import axiomic.quick_config as qc
            with qc.OpenAiGpt4:
                w = axiomic.Text('What is the capital of France?')
                assert w.infer().value() == 'Paris'


        .. code-block:: python

            history = [('Hello', 'Hi'), ('My Name is Victor', 'Nice to meet you')]
            w = axiomic.Text('Whats my name?')
            assert 'Victor' in w.infer(history_pairs=history_pairs).value()

        Args:
            system_prompt (str or Text): Optional, the system prompt to use for completion.
            history_pairs (List[Tuple[str or Text, str or Weave]]): Optional, pairs of chat history that should preceed this axiomic.
            name (str): Optional, the name of the new axiomic.

        Returns:
            A Text representing the completion.

        Raises:
            GraphError: If there was an error building this weave by the developer.
        '''
        history_pairs = lists.ChatList(history_pairs)

        m = self._merger()
        if system_prompt is None:
            system_prompt = m.autoweave(Text(''))
        else:
            system_prompt = m.autoweave(system_prompt)
        history_pair_nodes = []

        for pair in history_pairs:
            user = m.autoweave(pair.user)
            agent = m.autoweave(pair.agent)
            history_pair_nodes.append((user.node, agent.node))

        c = models.infer_context()
        complete_params = protos.axiomic.CompleteParams(
            llm_provider_name=c.llm_provider_name, llm_model_name=c.llm_model_name, 
            llm_temperature=c.llm_temperature, llm_max_tokens=c.llm_max_tokens,
        )
        return m.subweave(nF.complete(self.graph_builder, 
                                      self.node, 
                                      system_prompt.node, 
                                      history_pairs=history_pair_nodes, 
                                      complete_params=complete_params,
                                      name=name))

    def format(self, **inputs):
        '''
        Preforms string formatting on this axiomic. Either strings or weaves can be formatted.
        
        .. code-block:: python

            color = axiomic.Text('Blue')
            template = axiomic.Text('The sky is {sky_color} and the grass is {grass_color}')
            result = template.format(sky_color=color, grass_color='Green')
            assert result.value() == 'The sky is Blue and the grass is Green'

        Args:
            **inputs: Mapping of name to str or Text to format into this axiomic.

        Returns:
            A new Text that contains the values formatted together.

        Raises:
            GraphError: If formatting incorrectly.
        '''
        m = self._merger()
        boxed_inputs = {}
        for k, v in inputs.items():
            boxed_inputs[k] = m.autoweave(v).node
        return m.subweave(nF.format(self.graph_builder, self.node, **boxed_inputs))
    
    def name(self, name: str):
        m = self._merger()
        return m.subweave(nF.name_node(self.graph_builder, value=self.node, name=name))

    def _run(self):
        self._value = engine.eager_weft(self.graph_builder.get_graph(), self.node)

    def __str__(self):
        # TODO determine if we should allow str to implicitly value
        return self.__format__(None)
        # return str(self.value())

    def __repr__(self):
        return f'Text({self.node.name})'

    def value(self):
        '''
        Returns the string value of this axiomic. This may result in multple calls to
        multiple LLMs to resolve the value. Note: all previous calls were deferred
        until unaxiomic.
        
        .. code-block:: python

            w = axiomic.Text('What is the capital of France?')
            assert w.value() == 'What is the capital of France?'
            assert w.infer().value() == 'Paris'

        Returns:
            The string value of this axiomic.

        Raises:
            ThoughtCrime: If there was an error building this weave by the AI.
            GraphError: If there was an error building this weave by the developer.
        '''
        self._run()
        return self._value

    def value_json(self):
        '''
        values as a JSON, returning the value. Raises a GraphError if the value is not a valid JSON.
        You should consider using .validate_json(schema) instead if you want to ensure this is
        a valid JSON before unweaving it.
        
        .. code-block:: python

            w = axiomic.Text('{"name": "Alice"}')
            assert w.value_json()['name'] == 'Alice'

        Returns:
            The JSON value (dict, list, str, int, float, bool, or None) of this axiomic.

        Raises:
            GraphError: If the schema is not a valid JSON schema.
        '''
        return wjson.loads(self.value())

    def check(self, check):
        '''
        Checks this weave against the given check, returning either "true" or "false".

        Args:
            check: A check from the `axiomic.core.checks` module.

        Returns:
            A new Text (boolean, either "true" or "false") which indicates if this weave passes the check.
        '''
        m = self._merger()
        if check.is_core_unary_check():
            code = check.get_core_unary_check_code()
            return m.subweave(nF.core_unary_check(self.graph_builder, self.node, code))
        elif check.is_core_binary_check():
            code = check.get_core_binary_check_code()
            input_secondary = m.autoweave(check.get_input_secondary())
            return m.subweave(nF.builtin_binary_check(self.graph_builder, self.node, input_secondary.node, code))
        else:
            raise errors.GraphError('Not given a core unary or binary check')

    def checkpoint(self, check):
        '''
        Checkpoints this weave on the given check, causing a thought crime if the check fails.

        If the check succeeds, the weave returns itself.

        Args:
            check: A check from the `axiomic.core.checks` module.

        Returns:
            This axiomic.

        Raises:
            ThoughtCrime: If the check fails.
        '''
        m = self._merger()
        condition = m.autoweave(self.check(check))
        return m.subweave(nF.boolean_gate(self.graph_builder, self.node, condition.node))

    def validate_json(self, schema):
        '''
        Validates if this weave is a JSON which matches the given schema.

        Args:
            schema (str or Text): The schema to validate against.

        Returns:
            A new Text (boolean, either "true" or "false") which indicates if this weave follows the given JSON schema.

        Raises:
            GraphError: If the schema is not a valid JSON schema.
        '''
        m = self._merger()
        schema = m.autoweave(schema)
        return m.subweave(nF.check_json_schema(self.graph_builder, self.node, schema.node))

    def print_graph(self):
        '''
        Prints the execution graph of this weave to the console.
        '''
        engine.print_graph(self.graph_builder.get_graph(), self.node)

    def _rag_topk(self, rag_provider, k=3, separator='\n'):
        m = self._merger()
        rag_provider_name = rag_provider.get_provider_name()
        return m.subweave(nF.flat_rag_topk_query(self.graph_builder, self.node, separator=separator, k=k, rag_provider=rag_provider_name))

    def embed(self):
        c = models.infer_context()
        return embedding.TextEmbedding(self.node, c.embedding_provider_name, c.embedding_model_name, eager=self.eager)

    def _unsafe_access(self):
        '''Intenral use only - accesses the value without going through an unaxiomic.
        '''
        self._run()
        return self._value


TextType = typing.Union[str, Text]


class Merger:
    def __init__(self, eager=True):
        self.eager = eager
        self.weaves = []

    def __call__(self, w: Text):
        self.merge_from(w)
        return w
    
    def merge_from(self, w: Text):
        self.weaves.append(w)
    
    def merge_into(self, w: Text):
        for m in self.weaves:
            w.graph_builder.merge_from(m.graph_builder)
        return w

    def autoweave(self, thing: any):
        if is_json_type(thing):
            w = Text(json.dumps(thing), eager=self.eager)
            self.merge_from(w)
            return w
        if isinstance(thing, Text):
            self.merge_from(thing)
            return thing
        if thing is None:
            raise errors.GraphError('Cannot weave None')
        w = Text(thing, eager=self.eager)
        self.merge_from(w)
        return w

    def subweave(self, node):
        w = Text(node, eager=self.eager)

        self.merge_into(w)
        return w


JSON_TYPES = set([
    dict,
    list,
    # str, - doesn't count :)
    int,
    float,
    bool,
])

def is_json_type(thing: any):
    return type(thing) in JSON_TYPES
    

