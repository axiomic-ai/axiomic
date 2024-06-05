
import axiomic.protos as protos

from icecream import ic 


ic.configureOutput(includeContext=True)


def flat_rag_topk_node(node: protos.axiomic.FlatRagTopKNode, c, weave_node: protos.axiomic.AxiomicNode) -> str:
    query = c.resolve_node(node.query)
    separator = c.resolve_node(node.separator)
    rag_provider = c.get_provider(node.rag_provider)
    
    result_list = rag_provider.query_topk(query, k=node.k)
    result_str = separator.join(result_list)
    return result_str
