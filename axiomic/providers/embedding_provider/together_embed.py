

import time
from openai import OpenAI

import axiomic.providers.embedding_provider.embedding_provider as embedding_provider

client = OpenAI()

from typing import List
from together import Together

client = Together()

def embed(text, model) -> List[float]:
    start = time.time()
    text = text.replace("\n", " ")
    outputs = client.embeddings.create(model=model, input=[text])
    end = time.time()
    return outputs.data[0].embedding, end - start


class OpenAiLlmProviderImpl:
    def get_default_context_params(self):
        default_model = 'togethercomputer/m2-bert-80M-8k-retrieval'
        return {'embedding_provider_name': 'together_embed', 'embedding_model_name': default_model}

    def get_provider_name(self):
        return 'togther_embed'

    def infer(self, req: embedding_provider.EmbeddingRequest) -> embedding_provider.EmbeddingRequest:
        embedding, dur_s = embed(req.text, req.embedding_model_name)

        resp = embedding_provider.EmbeddingResponse(
            embedding_provider_name=req.embedding_provider_name,
            embedding_model_name=req.embedding_model_name,
            embedding=embedding,
            duration_s=dur_s
        )
        return resp


if __name__ == '__main__':
    print(embed('Hello, world!', 'togethercomputer/m2-bert-80M-8k-retrieval'))
