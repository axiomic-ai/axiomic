import dataclasses
import numpy as np


@dataclasses.dataclass
class AEmbedding:
    '''
    This is typed container for an embedding vector which offers some convience functionality.

    This is a stateless class.

    TODO: WIP. Under construction.
    '''
    vector: np.ndarray

    def cosine_similarity(self, other):
        if len(self.vector) != len(other.vector):
            raise ValueError('Embeddings must be of the same length')

        dot_product = np.dot(self.vector, other.vector)
        norm_vector1 = np.linalg.norm(self.vector)
        norm_vector2 = np.linalg.norm(other.vector)
        similarity = dot_product / (norm_vector1 * norm_vector2)
        return similarity

    def normalize_l2(self):
        norm = np.linalg.norm(self.vector)
        if norm == 0:
            raise ValueError('Cannot normalize a zero vector')
        return AEmbedding(vector=self.vector / norm)
