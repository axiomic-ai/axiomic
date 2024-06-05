
import axiomic.protos as protos

import json
import re


'''
message FormatInput {
    // The name of this input, for example, "my_name"
    string name = 1;

    // The value to format into the template, for example, "Victor"
    AxiomicNode value = 2;
}

message FormatNode {
    // A template, e.g. "Hello, my name is {my_name}."
    AxiomicNode template = 1;

    // The values to fill in the template, e.g. "name" -> "Victor".
    repeated FormatInput inputs = 2;
}
'''

KEY_REGEX = re.compile(r'{([a-zA-Z0-9_]+)}')

def detect_keys(text):
    return KEY_REGEX.findall(text)


def format_node(fn: protos.axiomic.FormatNode, context, weave_node: protos.axiomic.AxiomicNode) -> str:
    template = context.resolve_node(fn.template)
    inputs = fn.inputs
    # Replace the template with the values
    input_map = {}
    for i in inputs:
        name = i.name
        value = context.resolve_node(i.value)
        input_map[name] = value
    
    all_keys = detect_keys(template)
    missing_keys = set(all_keys) - set(input_map.keys())
    place_holders = {k: f'{{{k}}}' for k in missing_keys}
    input_map.update(place_holders)
    try:
        out = template.format(**input_map)
    except KeyError:
        raise ValueError(f'Failed to format template: {template} with inputs: {input_map}')
    return out

