import axiomic.models.context as context
import axiomic.models.generic as generic

Generic = generic.Generic

class OpenAI:

    class Text:
        GPT3_5 = context.LLMConfig(
            llm_provider_name='openai_text',
            llm_model_name='gpt-3.5-turbo',
            llm_temperature=0.5,
            llm_max_tokens=1024,
            _context_name='OpenAI.text.GPT3_5'
        )

        GPT4 = context.LLMConfig(
            llm_provider_name='openai_text',
            llm_model_name='gpt-4',
            llm_temperature=0.5,
            llm_max_tokens=1024,
            _context_name='OpenAI.text.GPT4'
        )

    class MultiModal:
        GPT4o = context.LLMConfig(
            llm_provider_name='openai_text',
            llm_model_name='gpt-4o',
            llm_temperature=0.5,
            llm_max_tokens=4096,
            _context_name='OpenAI.MultiModal.Gpt4o'
        )

    class Image:
        Dalle3_1024x1024 = context.Config(
            _context_name='OpenAiDalle3_1024x1024',
            image_provider_name='openai_img',
            image_model_name='dall-e-3',
            image_width=1024,
            image_height=1024
        )

        Dalle3_1024x1792 = context.Config(
            _context_name='OpenAiDalle3_1024x1792',
            image_model_name='dall-e-3',
            image_width=1024,
            image_height=1792
        )

        Dalle3_1792x1024 = context.Config(
            _context_name='OpenAiDalle3_1792x1024',
            image_model_name='dall-e-3',
            image_width=1792,
            image_height=1024
        )

    def bind():
        generic.bind(Generic.Text.Small, OpenAI.Text.GPT3_5)
        generic.bind(Generic.Text.Medium, OpenAI.Text.GPT3_5)
        generic.bind(Generic.Text.Large, OpenAI.MultiModal.GPT4o)
        generic.bind(Generic.Image.Medium, OpenAI.Image.Dalle3_1024x1024)

