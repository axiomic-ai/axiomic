

from typing import Any

import axiomic.errors as errors

class ProviderProvider:
    def __init__(self):
        self.providers = {}
        self.ref_store_provider = None

    def register_provider(self,  provider):
        self.providers[provider.get_provider_name()] = provider

    def get_provider(self, name) -> Any:
        if name not in self.providers:
            raise errors.WeaveError(f'Provider {name} not found.')
        return self.providers[name]
    
    def get_ref_store_provider(self):
        return self.ref_store_provider
    