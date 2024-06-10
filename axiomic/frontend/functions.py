
import axiomic.frontend.text as text

import axiomic.graph.serialize as serialize


def format(template: str, **kwargs) -> text.Text:
    '''
    See `axiomic.format` for more information.

    .. code-block:: python

        name = axiomic.Text('World')
        assert 'Hello, World!' == format('Hello, {name}!', name=name).value()

    '''
    return text.Text(template).format(**kwargs)

def infer(prompt: any, system_prompt=None, history_pairs=[], name=None) -> text.Text:
    '''
    Does text completion on the given prompt.

    The model used for completion is determined by the context, for example,

    .. code-block:: python

        import axiomic.quick_config as qc
        with qc.OpenAiGpt4:
            assert 'Pairs' in infer('What is the capital of France?').value()

    .. code-block:: python

        history = [('Hello', 'Hi'), 'My Name is Victor', 'Nice to meet you']
        w = infer('Whats my name?', history_pairs=history_pairs).value()
        assert 'Victor' in w.value()

    Args:
        system_prompt (str or Text): Optional, the system prompt to use for completion.
        history_pairs (List[Tuple[str or Txt, str or Text]]): Optional, pairs of chat history that should preceed this axiomic.
        name (str): Optional, the name of the new axiomic.

    Returns:
        Text representing the completion.

    Raises:
        GraphError: If there was an error building this graph by the developer.
    '''

    return text.Text(prompt).infer(system_prompt=system_prompt, history_pairs=history_pairs, name=name)


SerializableType = text.Text

def save(agent: SerializableType, path: str):
    '''
    Saves the agent to a file.

    .. code-block:: python

        agent = axiomic.Text('Hello, World!')
        axiomic.save(agent, 'hello_world.axiomic')

    Args:
        agent: The agent to save.
        path: The path to save the agent to.

    Raises:
        GraphError: If there was an error building this graph by the developer.
    '''
    serialize.graph_to_file(agent.get_graph(), path)


def load(path: str) -> text.Text:
    '''
    Loads an agent from a file.

    .. code-block:: python

        agent = axiomic.load('hello_world.axiomic')
        assert 'Hello, World!' == agent.value()

    Args:
        path: The path to load the agent from.

    Returns:
        The loaded agent.

    Raises:
        GraphError: If there was an error building this graph by the developer.
    '''
    graph = serialize.graph_from_file(path)
    return text.Text._from_graph(graph)
