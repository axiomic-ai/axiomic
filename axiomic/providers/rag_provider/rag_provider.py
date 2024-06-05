
import axiomic.logalytics as logalytics
import time

import axiomic.configure as configure


class RagProvider:
    '''
    Wrappr interface for all RAG implementations.
    '''

    def __init__(self, rag_impl):
        self.rag_impl = rag_impl
        configure.register_global_provider(self)

    def get_provider_name(self):
        return self.rag_impl.get_provider_name()

    def query_topk(self, query, k=3):

        with logalytics.RagQuery(self.get_provider_name(),
                             {'query': query,
                              'k': k,
                              'rag_provider': self.get_provider_name()}) as e:
            start = time.time()
            results = self.rag_impl.query(query, k)
            end = time.time()
            e.end(duration_s=end - start, k=k, results=results, rag_provider=self.get_provider_name())
        return results
