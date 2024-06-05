
import axiomic.providers.llm_provider.llm_provider as llm_provider
import axiomic.providers.llm_provider.anthropic_llm as anthropic_llm
import axiomic.providers.llm_provider.openai_llm as openai_llm
import axiomic.providers.param_provider.filesys_params as fs_params
import axiomic.providers.param_provider.param_provider as param_provider
import axiomic.providers.img_provider.img_provider as img_provider
import axiomic.providers.img_provider.openai_img as openai_img
import axiomic.providers.embedding_provider.openai_embed as openai_embed
import axiomic.providers.embedding_provider.embedding_provider as embedding_provider
import axiomic.providers.llm_provider.together_llm as together_llm
import axiomic.providers.img_provider.together_img as together_img


FILESYSTME_PARAMS = param_provider.ParamProvider(fs_params.FilesystemParamProviderImpl())
TOGETHER_LLM = llm_provider.LlmProvider(together_llm.TogetherProviderLlmImpl())
TOGETHER_IMG = img_provider.ImgProvider(together_img.TogetherImageProviderImpl())
ANTHROPIC_LLM = llm_provider.LlmProvider(anthropic_llm.AntropicLlmProvider())
OPENAI_LLM = llm_provider.LlmProvider(openai_llm.OpenAiLlmProvider())
OPENAI_IMG = img_provider.ImgProvider(openai_img.OpenAiImageProviderImpl())
OPENAI_EMBED = embedding_provider.EmbeddingProvider(openai_embed.OpenAiLlmProviderImpl())

