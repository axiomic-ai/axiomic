
import axiomic.protos as protos
import axiomic.errors as errors
import axiomic.engine.node_impls.builtin_unary_checks as builtin_unary_checks 


def builtin_unary_check_node(bucn: protos.axiomic.BuiltinUnaryCheckNode, context, weave_node: protos.axiomic.AxiomicNode) -> str:
    incoming_str = context.resolve_node(bucn.input)
    check_name = bucn.unary_check_name

    if check_name not in builtin_unary_checks.CHECKS:
        raise errors.WeaveError(f'Unknown check: {check_name}')

    answer = builtin_unary_checks.CHECKS[check_name](incoming_str)
    return answer
