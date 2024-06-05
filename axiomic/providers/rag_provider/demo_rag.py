import math
from collections import Counter

import re

import axiomic.providers.rag_provider.rag_provider as rag_provider



def split_doc(doc):
    words = re.sub(r'[^a-z0-9 \n]', '', doc.lower())
    parts = words.split()
    return parts



    

    

class TfidfVectorizer:
    def __init__(self):
        self.vocab = {}
        self.idf = {}

    def fit(self, documents):
        unique_words = set()
        for doc in documents:
            words = split_doc(doc)
            unique_words.update(words)

        self.vocab = {word: idx for idx, word in enumerate(unique_words)}

        N = len(documents)
        split_docs = [split_doc(doc) for doc in documents]
        for word in self.vocab:
            # df = sum(1 for doc in documents if word in split_doc(doc))
            df = sum(1 for doc in split_docs if word in doc)
            self.idf[word] = math.log(N / df)

    def transform(self, documents):
        vectors = []
        for doc in documents:
            words = split_doc(doc)
            word_counts = Counter(words)
            doc_len = len(words)

            vector = [0] * len(self.vocab)
            for word, count in word_counts.items():
                if word in self.vocab:
                    tf = count / doc_len
                    idx = self.vocab[word]
                    vector[idx] = tf * self.idf[word]

            vectors.append(vector)

        return vectors


def cosine_similarity(vec1, vec2):
    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    magnitude1 = math.sqrt(sum(a ** 2 for a in vec1))
    magnitude2 = math.sqrt(sum(b ** 2 for b in vec2))
    if magnitude1 == 0 or magnitude2 == 0:
        return 0
    else:
        return dot_product / (magnitude1 * magnitude2)


def get_nns_by_vector(query_vector, vectors, k):
    similarities = []
    for i, vector in enumerate(vectors):
        similarity = cosine_similarity(query_vector, vector)
        similarities.append((i, similarity))

    similarities.sort(key=lambda x: x[1], reverse=True)
    nearest_neighbors = [x[0] for x in similarities[:k]]
    return nearest_neighbors
    

class DemoRagProviderImpl:
    '''
    This is not suitable for production use. This is intended for Experiments, Demos and POCs only.

    This is a Demo implementation of a RAG Store.  
    It offers poor quality and slow performance, but it's very simple and portable.
    It is a top-k query across a corpus of text using TF-IDF vectorization and cosine similarity. 

    '''

    def __init__(self):
        self.vectorizer = TfidfVectorizer()
        self.texts = []
        self.vectors = []

        # Register Globally
        rag_provider.RagProvider(self)

    def get_provider_name(self):
        return f'Temporary#DemoRagProviderImpl-{id(self)}'

    def fit_texts(self, fit_texts):
        self.texts.extend(fit_texts)
        self.vectorizer.fit(self.texts)
        self.vectors = self.vectorizer.transform(self.texts)

    def query(self, query, k=3):
        query_words = split_doc(query)
        query_vector = [0] * len(self.vectorizer.vocab)

        for word in query_words:
            if word in self.vectorizer.vocab:
                idx = self.vectorizer.vocab[word]
                query_vector[idx] = self.vectorizer.idf[word]

        similar_indices = get_nns_by_vector(query_vector, self.vectors, k)
        return [self.texts[idx] for idx in similar_indices]


if __name__ == '__main__':
    # Sample usage
    texts = [
        "The quick brown fox jumps over the lazy dog",
        "The lazy dog sleeps all day long",
        "The quick brown fox is very quick and jumps high",
        "The dog is lazy and sleeps a lot",
        "The fox is brown and quick in jumping",
        "The cat is orange and prowls all day long",
        "The cat is very active and jumps high",
    ]

    rag = DemoRagProviderImpl()
    rag.fit_texts(texts)

    print(rag.query("orange cat jumps", k=3))
