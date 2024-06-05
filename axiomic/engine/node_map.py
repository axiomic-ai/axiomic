
import axiomic.engine.node_impls.immediate as immediate
import axiomic.engine.node_impls.history_complete as history_complete
import axiomic.engine.node_impls.format_node as format_node
import axiomic.engine.node_impls.boolean_gate as boolean_gate
import axiomic.engine.node_impls.flat_rag_topk_node as flat_rag_topk_node
import axiomic.engine.node_impls.name_node as name_node 
import axiomic.engine.node_impls.txt_to_img_node as txt_to_img_node
import axiomic.engine.node_impls.builtin_binary_check_node as builtin_binary_check_node
import axiomic.engine.node_impls.builtin_unary_check_node as builtin_unary_check_node


import axiomic.protos as protos


NODES = [
    ('immediate_node', protos.axiomic.ImmediateNode, immediate.immediate),
    # ('coerce_json_node', protos.axiomic.CoerceJsonNode, coerce_json.coerce_json),
    ('history_complete_node', protos.axiomic.HistoryCompleteNode, history_complete.history_complete),
    ('format_node', protos.axiomic.FormatNode, format_node.format_node),
    # ('custom_check_node', protos.axiomic.CustomCheckNode, custom_check.custom_check),
    ('boolean_gate_node', protos.axiomic.BooleanGateNode, boolean_gate.boolean_gate),
    # ('coerce_boolean_node', protos.axiomic.CoerceBooleanNode, coerce_boolean.coerce_boolean),
    ('flat_rag_top_k_node', protos.axiomic.FlatRagTopKNode, flat_rag_topk_node.flat_rag_topk_node),
    ('name_node', protos.axiomic.NameNode, name_node.name_node),
    ('text_to_images_node', protos.axiomic.TextToImagesNode, txt_to_img_node.txt_to_img_node),
    ('builtin_binary_check_node', protos.axiomic.BuiltinBinaryCheckNode, builtin_binary_check_node.builtin_binary_check_node),
    ('builtin_unary_check_node', protos.axiomic.BuiltinUnaryCheckNode, builtin_unary_check_node.builtin_unary_check_node)
]


def field_from_proto(proto):
    type_ = str(type(proto))
    for node in NODES:
        if type_ == str(node[1]):
            return node[0]

def exec_hook_by_field_name(field_name):
    for node in NODES:
        if field_name == node[0]:
            return node[2]

    raise Exception(f'No node found for field name {field_name}')



