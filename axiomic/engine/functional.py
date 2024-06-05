
import axiomic.protos as protos
import axiomic.engine as engine
import axiomic.engine.node_map as node_map
import axiomic.utils.naming as naming


COUNT = 0

def defualt_name(basename):
    global COUNT
    COUNT += 1
    basename = basename.replace('_node', '')
    return f'_{basename}{COUNT}'


class GraphBuilder:
    
    def __init__(self):
        self.nodes = []
        self.node_map = {}

    def get_graph(self):
        wg = protos.axiomic.AxiomicGraph()
        for node in self.nodes:
            wg.nodes.append(node)
        return wg

    def add_node(self, node: protos.axiomic.AxiomicNode):
        if node.name in self.node_map:
            return
        self.nodes.append(node)
        self.node_map[node.name] = node

    def upbox_node(self, node, name=None):
        if name is not None:
            name = naming.Name(name)
        field_name = node_map.field_from_proto(node)
        w = protos.axiomic.AxiomicNode()
        getattr(w, field_name).CopyFrom(node)
        if name:
            w.name = str(name)
        else:
            w.name = defualt_name(field_name)
        self.add_node(w)
        return w

    def autobox_as_node(self, anything, name=None):
        if isinstance(anything, str):
            return self.upbox_node(protos.axiomic.ImmediateNode(value=anything), name=name)

        if 'axiomic' in str(type(anything)):
            return anything
        
        anything_type = type(anything)
        raise Exception(f'Cannot autobox {anything_type}: {anything}')
    
    def merge_from(self, other):
        for node in other.nodes:
            if node.name not in self.node_map:
                self.add_node(node)

    def print_graph(self, root: protos.axiomic.AxiomicNode):
        return self.get_graph().print_tree(root)


def weave(gb: GraphBuilder, anything, name=None):
    node = gb.autobox_as_node(anything, name=name)
    gb.add_node(node)
    return node


def infer_image(gb: GraphBuilder, image_prompt: any, params: protos.axiomic.TextToImagesParams, name=None):
    prompt_node = gb.autobox_as_node(image_prompt)
    node = protos.axiomic.TextToImagesNode()
    node.image_prompt.name = prompt_node.name
    node.params.CopyFrom(params)
    return gb.upbox_node(node, name=name)


def complete(gb: GraphBuilder, context_window: any, system_prompt: any, complete_params: protos.axiomic.CompleteParams, history_pairs: any = [], name=None):
    context_window = gb.autobox_as_node(context_window)
    system_prompt = gb.autobox_as_node(system_prompt)

    flat_complete_node = protos.axiomic.HistoryCompleteNode()
    flat_complete_node.user_message.name = context_window.name
    flat_complete_node.system_prompt.name = system_prompt.name

    for user_msg, agent_msg in history_pairs:
        user_message = gb.autobox_as_node(user_msg)
        agent_message = gb.autobox_as_node(agent_msg)
        history_pair = protos.axiomic.ChatHistoryPair()
        history_pair.user_message.name = user_message.name
        history_pair.assistant_message.name = agent_message.name
        flat_complete_node.chat_history.append(history_pair)

    flat_complete_node.complete_params.CopyFrom(complete_params)
    n = gb.upbox_node(flat_complete_node, name=name)
    return n


def format(gb: GraphBuilder, template: any, **inputs):
    template = gb.autobox_as_node(template)
    format_node = protos.axiomic.FormatNode()
    format_node.template.name = template.name
    for k, v in inputs.items():
        boxed_v = gb.autobox_as_node(v)
        format_input = protos.axiomic.FormatInput(name=k)
        format_input.value.name = boxed_v.name
        format_node.inputs.append(format_input)
    return gb.upbox_node(format_node)


def coerce_json(gb: GraphBuilder, value: any):
    value = gb.autobox_as_node(value)
    coerce_json_node = protos.axiomic.CoerceJsonNode(json_ish=value)
    return gb.upbox_node(coerce_json_node)


def name_node(gb: GraphBuilder, value: any, name):
    value = gb.autobox_as_node(value)
    name_node = protos.axiomic.NameNode()
    name_node.input.name = value.name
    return gb.upbox_node(name_node, name=name)


def check_json_schema(gb: GraphBuilder, json_object: any, schema: any):
    return builtin_binary_check(gb, json_object, schema, protos.axiomic.BuiltinBinaryCheckNode.CHECK_JSONSCHEMA)


def builtin_binary_check(gb: GraphBuilder, input_main: any, input_secondary: any, binary_check_name: any):
    main = gb.autobox_as_node(input_main)
    secondary = gb.autobox_as_node(input_secondary)
    check_node = protos.axiomic.BuiltinBinaryCheckNode()
    check_node.input_main.name = main.name
    check_node.input_secondary.name = secondary.name
    check_node.binary_check_name = binary_check_name
    return gb.upbox_node(check_node)


def check_json_syntax(gb: GraphBuilder, json_object: any):
    return builtin_unary_check(gb, json_object, protos.axiomic.BuiltinUnaryCheckNode.CHECK_JSON_SYNTAX)


def core_unary_check(gb: GraphBuilder, input_value: any, unary_check_name: any):
    input_value = gb.autobox_as_node(input_value)
    check_node = protos.axiomic.BuiltinUnaryCheckNode()
    check_node.input.name = input_value.name
    check_node.unary_check_name = unary_check_name
    return gb.upbox_node(check_node)


def flat_rag_topk_query(gb: GraphBuilder, query: any, separator: any, k: int, rag_provider: str):
    query = gb.autobox_as_node(query)
    seperator = gb.autobox_as_node(separator)
    rag_node = protos.axiomic.FlatRagTopKNode()

    rag_node.query.name = query.name
    rag_node.separator.name = seperator.name
    rag_node.k = k
    rag_node.rag_provider = rag_provider
    return gb.upbox_node(rag_node)


def coerce_boolean(gb: GraphBuilder, value: any):
    value = gb.autobox_as_node(value)
    coerce_boolean_node = protos.axiomic.CoerceBooleanNode(boolean_ish=value)
    # FXIME - make this configurable
    coerce_boolean_node.uncertain_mode = protos.axiomic.CoerceBooleanNode.UNCERTAIN_IS_THOUGHT_CRIME
    return gb.upbox_node(coerce_boolean_node)


def boolean_gate(gb: GraphBuilder, boolean: any, gating: any):
    boolean = gb.autobox_as_node(boolean)
    gating = gb.autobox_as_node(gating)

    boolean_gate_node = protos.axiomic.BooleanGateNode()

    boolean_gate_node.value.name = boolean.name
    boolean_gate_node.gating.name = gating.name

    return gb.upbox_node(boolean_gate_node)
