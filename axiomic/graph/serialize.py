
import axiomic.protos as protos


def graph_to_file(graph: protos.axiomic.AxiomicGraph, file_path: str):
    '''
    Saves the graph to a file.
    '''
    protos.file_dump(graph, file_path)


def graph_from_file(file_path: str) -> protos.axiomic.AxiomicGraph:
    '''
    Loads the graph from a file.
    '''
    graph = protos.axiomic.AxiomicGraph()
    protos.file_parse(graph, file_path)
    return graph
