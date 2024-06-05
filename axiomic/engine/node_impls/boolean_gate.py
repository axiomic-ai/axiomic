

import axiomic.protos as protos

import axiomic.errors as errors
import axiomic.constants as constants

VALUES_FOR_TRUE = [
    constants.TRUE_VALUE
]

def boolean_gate(bgn: protos.axiomic.BooleanGateNode, context, weave_node: protos.axiomic.AxiomicNode) -> str:
    value = context.resolve_node(bgn.value)
    gating = context.resolve_node(bgn.gating)

    if gating in VALUES_FOR_TRUE:
        return value

    raise errors.ThoughtCrime(f'Boolean Gated Failed: Expected Gating to be "True". Gate=<{gating}> Blocking Value=<{value}>')
