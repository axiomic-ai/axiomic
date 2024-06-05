
import axiomic.models.context as context
import axiomic.models.generic as generic


Generic = generic.Generic

# TogetherStableDiffusion_XL_Base_1_0 = context.Config(
#     image_provider_name='together_text',
#     image_model_name='stabilityai/stable-diffusion-xl-base-1.0'
# )
# 
# TogetherLlama3_8B_Chat = context.LLMConfig(
#     llm_provider_name='together_text',
#     llm_model_name='meta-llama/Llama-3-8b-chat-hf'
# )
# 
# TogetherLlama3_70B = context.LLMConfig(
#     llm_provider_name='together_text',
#     llm_model_name='meta-llama/Meta-Llama-3-70B'
# )
# 
# TogetherQuen1_5_35B_Chat = context.LLMConfig(
#     llm_provider_name='together_text',
#     llm_model_name='Qwen/Qwen1.5-32B-Chat'
# )

def TogetherChat(model):
    return context.LLMConfig(llm_provider_name='together_text', llm_model_name=model)

def TogetherEmbedding(model):
    # FIXME
    return context.Config(llm_provider_name='together_text', llm_model_name=model)

def TogetherImage(model):
    return context.Config(image_provider_name='together_img', image_model_name=model)

def TogetherCode(model):
    return context.Config(llm_provider_name='together_text', llm_model_name=model)

def TogetherLanguage(model):
    return context.Config(llm_provider_name='together_text', llm_model_name=model)

def TogetherModeration(model):
    return context.Config(llm_provider_name='together_text', llm_model_name=model)


class Together:

  class Text:

    class Austism:
      chronos_hermes_13b = TogetherChat("Austism/chronos-hermes-13b")

    class Nexusflow:
      nexusraven_v2_13b = TogetherChat("Nexusflow/NexusRaven-V2-13B")

    class NousResearch:
      nous_capybara_7b_v1p9 = TogetherChat("NousResearch/Nous-Capybara-7B-V1p9")
      nous_hermes_2_mistral_7b_dpo = TogetherChat("NousResearch/Nous-Hermes-2-Mistral-7B-DPO")
      nous_hermes_2_mixtral_8x7b_dpo = TogetherChat("NousResearch/Nous-Hermes-2-Mixtral-8x7B-DPO")
      nous_hermes_2_mixtral_8x7b_sft = TogetherChat("NousResearch/Nous-Hermes-2-Mixtral-8x7B-SFT")
      nous_hermes_2_yi_34b = TogetherChat("NousResearch/Nous-Hermes-2-Yi-34B")
      nous_hermes_llama2_13b = TogetherChat("NousResearch/Nous-Hermes-Llama2-13b")
      nous_hermes_llama_2_7b = TogetherChat("NousResearch/Nous-Hermes-llama-2-7b")

    class OpenOrca:
      mistral_7b_openorca = TogetherChat("Open-Orca/Mistral-7B-OpenOrca")

    class Phind:
      phind_codellama_34b_v2 = TogetherChat("Phind/Phind-CodeLlama-34B-v2")

    class Qwen:
      qwen1_5_0_5b = TogetherChat("Qwen/Qwen1.5-0.5B")
      qwen1_5_1_8b = TogetherChat("Qwen/Qwen1.5-1.8B")
      qwen1_5_110b_chat = TogetherChat("Qwen/Qwen1.5-110B-Chat")
      qwen1_5_14b = TogetherChat("Qwen/Qwen1.5-14B")
      qwen1_5_32b = TogetherChat("Qwen/Qwen1.5-32B")
      qwen1_5_4b = TogetherChat("Qwen/Qwen1.5-4B")
      qwen1_5_72b = TogetherChat("Qwen/Qwen1.5-72B")
      qwen1_5_7b = TogetherChat("Qwen/Qwen1.5-7B")

    class AllenAI:
      olmo_7b = TogetherChat("allenai/OLMo-7B")
      olmo_7b_twin_2t = TogetherChat("allenai/OLMo-7B-Twin-2T")

    class DeepseekAI:
      deepseek_llm_67b_chat = TogetherChat("deepseek-ai/deepseek-llm-67b-chat")

    class GarageBaind:
      platypus2_70b_instruct = TogetherChat("garage-bAInd/Platypus2-70B-instruct")

    class Google:
      gemma_2b = TogetherChat("google/gemma-2b")
      gemma_7b_it = TogetherChat("google/gemma-7b-it")

    class Microsoft:
      wizardlm_2_8x22b = TogetherChat("microsoft/WizardLM-2-8x22B")
      phi_2 = TogetherChat("microsoft/phi-2")

    class MistralAI:
      mistral_7b_instruct_v0_2 = TogetherChat("mistralai/Mistral-7B-Instruct-v0.2")
      mistral_7b_v0_1 = TogetherChat("mistralai/Mistral-7B-v0.1")
      mixtral_8x22b = TogetherChat("mistralai/Mixtral-8x22B")
      mixtral_8x7b_v0_1 = TogetherChat("mistralai/Mixtral-8x7B-v0.1")
      mistral_7b_instruct_v0_1 = TogetherLanguage("mistralai/Mistral-7B-Instruct-v0.1")
      mixtral_8x22b_instruct_v0_1 = TogetherLanguage("mistralai/Mixtral-8x22B-Instruct-v0.1")
      mixtral_8x7b_instruct_v0_1 = TogetherLanguage("mistralai/Mixtral-8x7B-Instruct-v0.1")

    class Openchat:
      openchat_3_5_1210 = TogetherChat("openchat/openchat-3.5-1210")

    class SnorkelAI:
      snorkel_mistral_pairrm_dpo = TogetherChat("snorkelai/Snorkel-Mistral-PairRM-DPO")

    class Teknium:
      openhermes_2_mistral_7b = TogetherChat("teknium/OpenHermes-2-Mistral-7B")
      openhermes_2p5_mistral_7b = TogetherChat("teknium/OpenHermes-2p5-Mistral-7B")

    class Together:
      gpt_jt_moderation_6b = TogetherChat("togethercomputer/GPT-JT-Moderation-6B")
      llama_2_7b_32k = TogetherChat("togethercomputer/LLaMA-2-7B-32K")
      redpajama_incite_7b_base = TogetherChat("togethercomputer/RedPajama-INCITE-7B-Base")
      stripedhyena_hessian_7b = TogetherChat("togethercomputer/StripedHyena-Hessian-7B")
      stripedhyena_nous_7b = TogetherChat("togethercomputer/StripedHyena-Nous-7B")

    class ZeroOneAI:
      yi_34b_chat = TogetherChat("zero-one-ai/Yi-34B-Chat")

    class Qwen:
      qwen1_5_0_5b_chat = TogetherLanguage("Qwen/Qwen1.5-0.5B-Chat")
      qwen1_5_1_8b_chat = TogetherLanguage("Qwen/Qwen1.5-1.8B-Chat")
      qwen1_5_14b_chat = TogetherLanguage("Qwen/Qwen1.5-14B-Chat")
      qwen1_5_32b_chat = TogetherLanguage("Qwen/Qwen1.5-32B-Chat")
      qwen1_5_4b_chat = TogetherLanguage("Qwen/Qwen1.5-4B-Chat")
      qwen1_5_72b_chat = TogetherLanguage("Qwen/Qwen1.5-72B-Chat")
      qwen1_5_7b_chat = TogetherLanguage("Qwen/Qwen1.5-7B-Chat")

    class Snowflake:
      snowflake_arctic_instruct = TogetherLanguage("Snowflake/snowflake-arctic-instruct")

    class AllenAI:
      olmo_7b_instruct = TogetherLanguage("allenai/OLMo-7B-Instruct")

    class CodeLlama:
      codellama_7b_python_hf = TogetherLanguage("codellama/CodeLlama-7b-Python-hf")

    class Cognitive:
      dolphin_2_5_mixtral_8x7b = TogetherLanguage("cognitivecomputations/dolphin-2.5-mixtral-8x7b")

    class DataBricks:
      dbrx_instruct = TogetherLanguage("databricks/dbrx-instruct")

    class DeepseekAi:
      deepseek_coder_33b_instruct = TogetherLanguage("deepseek-ai/deepseek-coder-33b-instruct")

    class Google:
      gemma_2b_it = TogetherLanguage("google/gemma-2b-it")
      gemma_7b = TogetherLanguage("google/gemma-7b")
    
    class Llama3:
      llama_3_8b_chat_hf = TogetherLanguage("meta-llama/Llama-3-8b-chat-hf")
      llama_3_8b_hf = TogetherChat("meta-llama/Llama-3-8b-hf")
      llama_3_70b_chat_hf = TogetherChat("meta-llama/Llama-3-70b-chat-hf")
      meta_llama_3_70b = TogetherLanguage("meta-llama/Meta-Llama-3-70B")

    class Llama2:
      llama_2_13b_hf = TogetherLanguage("meta-llama/Llama-2-13b-hf")
      llama_2_70b_hf = TogetherLanguage("meta-llama/Llama-2-70b-hf")
      llama_2_7b_chat_hf = TogetherLanguage("meta-llama/Llama-2-7b-chat-hf")
      llama_2_13b_chat_hf = TogetherChat("meta-llama/Llama-2-13b-chat-hf")
      llama_2_70b_chat_hf = TogetherChat("meta-llama/Llama-2-70b-chat-hf")
      llama_2_7b_hf = TogetherChat("meta-llama/Llama-2-7b-hf")
      llama_guard_7b = TogetherChat("Meta-Llama/Llama-Guard-7b")
      llamaguard_2_8b = TogetherChat("meta-llama/LlamaGuard-2-8b")

    class CodeLlama:
      codellama_13b_instruct_hf = TogetherCode("codellama/CodeLlama-13b-Instruct-hf")
      codellama_34b_instruct_hf = TogetherCode("codellama/CodeLlama-34b-Instruct-hf")
      codellama_70b_instruct_hf = TogetherCode("codellama/CodeLlama-70b-Instruct-hf")
      codellama_70b_python_hf = TogetherCode("codellama/CodeLlama-70b-Python-hf")
      codellama_7b_instruct_hf = TogetherCode("codellama/CodeLlama-7b-Instruct-hf")
      codellama_70b_hf = TogetherModeration("codellama/CodeLlama-70b-hf")
      codellama_13b_python_hf = TogetherChat("codellama/CodeLlama-13b-Python-hf")
      codellama_34b_python_hf = TogetherChat("codellama/CodeLlama-34b-Python-hf")

    # FIXME: Broken
    # class PromptHero:
    #  openjourney = TogetherLanguage("prompthero/openjourney")

    class Togethercomputer:
      llama_2_7b_32k_instruct = TogetherLanguage("togethercomputer/Llama-2-7B-32K-Instruct")
      redpajama_incite_7b_instruct = TogetherLanguage("togethercomputer/RedPajama-INCITE-7B-Instruct")
      redpajama_incite_chat_3b_v1 = TogetherLanguage("togethercomputer/RedPajama-INCITE-Chat-3B-v1")
      redpajama_incite_instruct_3b_v1 = TogetherLanguage("togethercomputer/RedPajama-INCITE-Instruct-3B-v1")
      evo_1_131k_base = TogetherLanguage("togethercomputer/evo-1-131k-base")
      evo_1_8k_base = TogetherLanguage("togethercomputer/evo-1-8k-base")

    class ZeroOneAI:
      yi_34b = TogetherLanguage("zero-one-ai/Yi-34B")
      yi_6b = TogetherLanguage("zero-one-ai/Yi-6B")

    class Wizardlm:
      wizardlm_13b_v1_2 = TogetherCode("WizardLM/WizardLM-13B-V1.2")

    class Lmsys:
      vicuna_13b_v1_5 = TogetherCode("lmsys/vicuna-13b-v1.5")

  class Embedding:

    class Baai:
      bge_base_en_v1_5 = TogetherEmbedding("BAAI/bge-base-en-v1.5")
      bge_large_en_v1_5 = TogetherEmbedding("BAAI/bge-large-en-v1.5")

    class WhereIsAI:
      uae_large_v1 = TogetherEmbedding("WhereIsAI/UAE-Large-V1")

    class SentenceTransformers:
      msmarco_bert_base_dot_v5 = TogetherEmbedding("sentence-transformers/msmarco-bert-base-dot-v5")

    class Together:
      m2_bert_80m_2k_retrieval = TogetherEmbedding("togethercomputer/m2-bert-80M-2k-retrieval")
      m2_bert_80m_32k_retrieval = TogetherEmbedding("togethercomputer/m2-bert-80M-32k-retrieval")
      m2_bert_80m_8k_retrieval = TogetherEmbedding("togethercomputer/m2-bert-80M-8k-retrieval")

    class Upstage:
      solar_10_7b_instruct_v1_0 = TogetherEmbedding("upstage/SOLAR-10.7B-Instruct-v1.0")

  class Image:

    class Sg161222:
      realisticvisionv3_0vae = TogetherChat("SG161222/Realistic_Vision_V3.0_VAE")

    class Wizardlm:
      wizardcoder_python_34b_v1_0 = TogetherImage("WizardLM/WizardCoder-Python-34B-V1.0")

    class StabilityAI:
      stable_diffusion_2_1 = TogetherImage("stabilityai/stable-diffusion-2-1")
      stable_diffusion_xl_base_1_0 = TogetherImage("stabilityai/stable-diffusion-xl-base-1.0")

    class Togethercomputer:
      redpajama_incite_base_3b_v1 = TogetherImage("togethercomputer/RedPajama-INCITE-Base-3B-v1")
      alpaca_7b = TogetherImage("togethercomputer/alpaca-7b")


  def bind():
    generic.bind(Generic.Text.Small, Together.Text.Llama3.llama_3_8b_chat_hf)
    generic.bind(Generic.Text.Medium, Together.Text.Qwen.qwen1_5_32b_chat)
    generic.bind(Generic.Text.Large, Together.Text.Llama3.llama_3_70b_chat_hf)
    generic.bind(Generic.Image.Medium, Together.Image.StabilityAI.stable_diffusion_2_1)

