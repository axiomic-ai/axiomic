
import axiomic.models.context as context
import axiomic.models.generic as generic

Generic = generic.Generic
Config = context.Config

class Google:

    class Text:

        class Gemini:

            ''' Default Opus, you need to also `export GOOGLE_API_KEY=sk-...` '''
            Pro = Config(
                llm_provider_name='google_text',
                llm_model_name='gemini-2.5-pro-exp-03-25',
                llm_temperature=0.5,
                llm_max_tokens=1024,
                _context_name='GeminiPro'
            )

            ''' Default Sonnet, you need to also `export GOOGLE_API_KEY=sk-...` '''
            Flash = Config(
                llm_provider_name='google_text',
                llm_model_name='gemini-2.0-flash',
                llm_temperature=0.5,
                llm_max_tokens=1024,
                _context_name='GeminiFlash'
            )

            ''' Default Haiku, you need to also `export GOOGLE_API_KEY=sk-...` '''
            FlashLite = Config(
                llm_provider_name='google_text',
                llm_model_name='gemini-2.0-flash-lite',
                llm_temperature=0.5,
                llm_max_tokens=1024,
                _context_name='GeminiFlashLite'
            )
    
    def bind():
        generic.bind(Generic.Text.Small, Google.Text.Gemini.FlashLite)
        generic.bind(Generic.Text.Medium, Google.Text.Gemini.Flash)
        generic.bind(Generic.Text.Large, Google.Text.Gemini.Pro)

