

import time
from openai import OpenAI

import axiomic.providers.embedding_provider.embedding_provider as embedding_provider

import os


if "OPENAI_API_KEY" in os.environ:
    client = OpenAI()
else:
    client = None


def embed(text, model_name):
    start = time.time()
    message = client.embeddings.create(
        input=text,
        model=model_name
    )
    end = time.time()
    return message.data[0].embedding, end - start


class OpenAiLlmProviderImpl:
    def get_default_context_params(self):
        default_model = 'text-embedding-3-small' # 'text-embedding-ada-002' #  # 
        return {'embedding_provider_name': 'openai_embed', 'embedding_model_name': default_model}

    def get_provider_name(self):
        return 'openai_embed'

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
    print(embed('Hello, world!', 'text-embedding-ada-002'))