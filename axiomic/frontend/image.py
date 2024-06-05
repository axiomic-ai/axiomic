
import axiomic.errors as errors
import axiomic.engine.functional as nF
import axiomic.protos as protos
import axiomic.engine as engine
import axiomic.data.aimage as wimage


class Image:
    '''
    An Image. Do not call the constructor.
    '''
    def __init__(self, node: any, eager=False, name=None):
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
            raise errors.WeaveError('Image must be constructed from a weave graph node.')

    def infer(self):
        '''
        Not Implemented Yet. Image to text coming soon.
        '''
        raise NotImplementedError('Image Weaves do not support infer yet: Infer on images not implemented yet')

    def _run(self):
        if self._value is None:
            self._value = engine.eager_weft(self.graph_builder.get_graph(), self.node)

    def __str__(self):
        return self.value()

    def __repr__(self):
        return f'Image({self.node.name})'

    def value(self):
        '''
        Returns:
            The image as a WImage.
        '''
        self._run()
        return self.value_image()

    def print_graph(self):
        engine.print_graph(self.graph_builder.get_graph(), self.node)

    def value_image(self, index=0):
        '''
        Returns:
            The image as a WImage.
        '''
        self._run()
        return self._value[index]

    def print(self):
        '''
        Prints the image to the terminal.
        '''
        self._run()
        for img in self._value:
            img.print()
        return self
