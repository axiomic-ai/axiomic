
import axiomic.errors as errors
import axiomic.engine.functional as nF
import axiomic.protos as protos
import axiomic.engine as engine
import axiomic.data.aembedding as wembedding

import axiomic.providers.embedding_provider.embedding_provider as embedding_provider

import axiomic.configure as configure


class Embedding:
    '''
    An Image Weave. Do not call the constructor.
    '''
    def __init__(self, node: any, embedding_provider_name, embedding_model_name, eager=False, name=None):
        self.embedding_provider_name = embedding_provider_name
        self.embedding_model_name = embedding_model_name
        self.eager = eager
        # self.nav_breadcrumbs = nav_breadcrumbs
        self._value = None
        self.graph_builder = nF.GraphBuilder()
        self.given_name = name
        #if isinstance(node, Weave):
        #    raise errors.WeaveError('Image Weaves cannot be created from Weave objects.')
        if isinstance(node, protos.axiomic.AxiomicNode):
            self.node = node
            self.graph_builder.add_node(self.node)
            if name is not None:
                if name != node.name:
                    raise NotImplementedError('Name passing not supported yet')
        else:
            raise errors.WeaveError('WeaveImage must be constructed from a weave graph node.')

    def _run(self):
        if self._value is None:
            self._value = engine.eager_weft(self.graph_builder.get_graph(), self.node)

    def __str__(self):
        return self.value()

    def __repr__(self):
        return f'WeaveImage({self.node.name})'

    def unweave(self):
        '''
        Returns:
            The embedding as WEmbedding
        '''
        return self.unweave_embedding()

    def unweave_embedding(self):
        self._run()
        c = configure.infer_context()
        prov = c.provider_provider.get_provider(self.embedding_provider_name)
        req = embedding_provider.EmbeddingRequest(embedding_provider_name=self.embedding_provider_name, embedding_model_name=self.embedding_model_name, text=self._value)
        resp = prov.infer(req)
        return wembedding.WEmbedding(resp.embedding)

    def print_graph(self):
        engine.print_graph(self.graph_builder.get_graph(), self.node)

    def print(self):
        '''
        Prints the image to the terminal.
        '''
        self._run()
        for img in self._value:
            img.print()
        return self

