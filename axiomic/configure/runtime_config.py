

import dataclasses


@dataclasses.dataclass
class RuntimeConfig:
    small_text_provider: str = None
    small_text_model: str = None

    medium_text_provider: str = None
    medium_text_model: str = None

    large_text_provider: str = 'openai_llm'
    large_text_model: str = 'gpt-4'

    medium_image_provider: str = None
    medium_image_model: str = None
    medium_image_width: int = None
    medium_image_height: int = None


GLBOAL_RUNTIME_CONFIG = RuntimeConfig()


def resolve_runtime_provider_and_model(runtime_provider, runtime_model):
    if 'RUNTIME:' not in runtime_provider:
        raise NotImplementedError('Only RUNTIME: providers are supported')
    if 'RUNTIME:' not in runtime_model:
        raise NotImplementedError('Only RUNTIME: models are supported')

    runtime_provider = runtime_provider.replace('RUNTIME:', '')
    runtime_model = runtime_model.replace('RUNTIME:', '')

    prov = getattr(GLBOAL_RUNTIME_CONFIG, f'{runtime_provider}')
    model = getattr(GLBOAL_RUNTIME_CONFIG, f'{runtime_model}')
    return prov, model
