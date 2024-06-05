
import axiomic.protos as protos

def name_node(fn: protos.axiomic.NameNode, context, weave_node: protos.axiomic.AxiomicNode) -> str:
    input_ = context.resolve_node(fn.input)
    return input_
