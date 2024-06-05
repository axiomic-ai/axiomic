
import axiomic.protos as protos
import axiomic.errors as errors
import axiomic.engine.node_impls.builtin_binary_checks as builtin_binary_checks 


def builtin_binary_check_node(bucn: protos.axiomic.BuiltinBinaryCheckNode, context, weave_node: protos.axiomic.AxiomicNode) -> str:
    incoming_str = context.resolve_node(bucn.input_main)
    secondary_str  = context.resolve_node(bucn.input_secondary)
    binary_check_name = bucn.binary_check_name

    if binary_check_name not in builtin_binary_checks.CHECKS:
        raise errors.WeaveError(f'Unknown builtin binary check: {binary_check_name}')

    answer = builtin_binary_checks.CHECKS[binary_check_name](incoming_str, secondary_str)
    return answer
