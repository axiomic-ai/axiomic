

import axiomic.protos as protos



def immediate(i: protos.axiomic.ImmediateNode, context, weave_node: protos.axiomic.AxiomicNode) -> str:
    return i.value
