
import axiomic.models.context as context
import axiomic.models.generic as generic

Generic = generic.Generic
Config = context.Config

class Anthropic:

    class Text:

        class Claude3:

            ''' Default Opus, you need to also `export ANTHROPIC_API_KEY=sk-...` '''
            Opus = Config(
                llm_provider_name='anthropic_text',
                llm_model_name='claude-3-opus-20240229',
                llm_temperature=0.5,
                llm_max_tokens=1024,
                _context_name='AnthropicOpus'
            )

            ''' Default Sonnet, you need to also `export ANTHROPIC_API_KEY=sk-...` '''
            Sonnet = Config(
                llm_provider_name='anthropic_text',
                llm_model_name='claude-3-sonnet-20240229',
                llm_temperature=0.5,
                llm_max_tokens=1024,
                _context_name='AnthropicSonnet'
            )

            ''' Default Haiku, you need to also `export ANTHROPIC_API_KEY=sk-...` '''
            Haiku = Config(
                llm_provider_name='anthropic_text',
                llm_model_name='claude-3-haiku-20240307',
                llm_temperature=0.5,
                llm_max_tokens=1024,
                _context_name='AnthropicHaiku'
            )
    
    def bind():
        generic.bind(Generic.Text.Small, Anthropic.Text.Claude3.Haiku)
        generic.bind(Generic.Text.Medium, Anthropic.Text.Claude3.Sonnet)
        generic.bind(Generic.Text.Large, Anthropic.Text.Claude3.Opus)

