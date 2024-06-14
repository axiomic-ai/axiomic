
import axiomic.protos as protos

import json
import re

import axiomic.constants as constants


def conditional_node(fn: protos.axiomic.ConditionalNode, context, weave_node: protos.axiomic.AxiomicNode) -> str:
    check = context.resolve_node(fn.check)

    if check == constants.TRUE_VALUE:
        return context.resolve_node(fn.true_branch)
    if check == constants.FALSE_VALUE:
        return context.resolve_node(fn.false_branch)
    
    raise ValueError(f'Conditional check failed: Expected check to be {constants.TRUE_VALUE} or {constants.FALSE_VALUE}. Check=<{check}>')
