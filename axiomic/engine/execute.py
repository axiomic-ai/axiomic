

from typing import Any
import axiomic.protos as protos

import axiomic.engine.node_map as node_map
# import axiomic.context as context
import axiomic.models.context as wcontext

import axiomic.engine.exec_context as exec_context

import axiomic.graph.tree as tree
import axiomic.errors as errors
import axiomic.core_config as core_config
import hashlib
import axiomic.logalytics.sink as sink
import axiomic.logalytics.events as events


global_context = exec_context.ExecutionContext()


def md5sum_string(input_string):
    return hashlib.md5(input_string.encode()).hexdigest()


def hash_node(node: protos.axiomic.AxiomicNode) -> str:
    return md5sum_string(str(node))


class WeftContext:
    def __init__(self, graph: protos.axiomic.AxiomicGraph, exec_context: exec_context.ExecutionContext, config: core_config.Config):
        self.exec_context = exec_context
        self.retry_thought_crime_count = config.thought_crime_retry_count
        self._weft_cache = {}
        self.graph = tree.Graph(graph)

    def is_cached(self, node: any) -> bool:
        if hash_node(node) in self._weft_cache:
            return True
        if not core_config.global_config.enable_caching:
            return False
        ans = self.exec_context.is_cached(node)
        return ans

    def get_cached(self, node: any) -> str:
        if hash_node(node) in self._weft_cache:
            return self._weft_cache[hash_node(node)]

        if not core_config.global_config.enable_caching:
            raise Exception('Caching is disabled')

        return self.exec_context.get_cached(node)

    def cache_put(self, node: any, output: str):
        root_hash = hash_node(node)
        self._weft_cache[hash_node(node)] = output
        if not core_config.global_config.enable_caching:
            return
        self.exec_context.cache_put(node, output)

    def posion_cache(self, node: any):
        if hash_node(node) in self._weft_cache:
            del self._weft_cache[hash_node(node)]
        
        if not core_config.global_config.enable_caching:
            return
        self.exec_context.posion_cache(node)

    def resolve_node(self, node: any) -> str:
        if str(type(node)) == str(protos.axiomic.NodeRef):
            node = self.graph.ref_to_node(node)
        if not self.is_cached(node):
            raise Exception('Node not cached? Internal Error: ' + node.name)
        return self.get_cached(node)

    def get_provider(self, provider_name: str) -> Any:
        return wcontext.infer_context().provider_provider.get_provider(provider_name)
        

def print_graph(graph: protos.axiomic.AxiomicGraph, root: protos.axiomic.AxiomicNode):
    g = tree.Graph(graph)
    g.print_tree(root)

def eager_weft(graph: protos.axiomic.AxiomicGraph, node: protos.axiomic.AxiomicNode) -> str:
    weft = Weft(WeftContext(graph, global_context, config=core_config.global_config))
    global_context.flush_cache()
    return weft.exec_node(node)


class Weft:
    def __init__(self, context: WeftContext):
        self.context = context

    def _cache_node_output(self, node: protos.axiomic.AxiomicNode):
        if self.context.is_cached(node):
            return
        output = resolve_node(node, self.context)
        self.context.cache_put(node, output)

    def exec_node(self, node: protos.axiomic.AxiomicNode, blocking=True) -> str:
        if self.context.is_cached(node):
            return self.context.get_cached(node)

        tries_left = 1 + self.context.retry_thought_crime_count
        while tries_left > 0:
            try:
                root_hash = hash_node(node)
                self._flatten_and_cache_tree(node)
                # All nodes should be cached in the tree now. Let's get the root.

                if not self.context.is_cached(node):
                    raise Exception(f'Root node not cached??? {node.name} # {root_hash}')
                out = self.context.get_cached(node)
                return out
            except errors.ThoughtCrime as e:
                print('Weft: ThoughtCrime: ', e)
                tries_left -= 1
                if tries_left == 0:
                    raise e
                self._posion_cache(node)
                sink.event_sink(events.Event('Retry ThoughtCrime', events.EventType.THOUGHT_CRIME_RETRY, {'message': 'thought crime occured - retrying query.'}))

        raise Exception('Unreachable')

    def _posion_cache(self, node: protos.axiomic.AxiomicNode):
        # recursively removes this tree from the cache.
        all_nodes = tree.reversed_breadth_first_flatten(self.context.graph, node)
        for node in all_nodes:
            self.context.posion_cache(node)

    def _flatten_and_cache_tree(self, node: protos.axiomic.AxiomicNode):
        all_nodes = self.context.graph.flatten_node(node)
        for node in all_nodes:
            self._cache_node_output(node)

    def _exec_node(self, node: protos.axiomic.AxiomicNode, blocking=True) -> str:
        if not blocking:
            raise Exception('Non-blocking execution not supported yet')
        return resolve_node(node, self.context)


def get_context():
    c = context.Context()
    c.set_node_resolver(resolve_node)
    return c


def resolve_node(node: protos.axiomic.AxiomicNode, c: WeftContext) -> str:
    type_name = str(type(node))
    if type_name != str(protos.axiomic.AxiomicNode):
        raise Exception(type_name)

    field_name = node.WhichOneof('node_type')
    sub_node = getattr(node, field_name)
    output = node_map.exec_hook_by_field_name(field_name)(sub_node, c, node)
    return output


def run(node: any) -> str:
    return resolve_node(node, get_context())

