
import axiomic.models as configure

import axiomic.logalytics.explainers as explainers

from axiomic.frontend.text import Text
import axiomic.errors as errors


# Maps param names to text
PARAM_MAP = { }


def is_bucket(param_ref: str) -> bool:
    ref_provider = configure.infer_context().provider_provider.ref_store_provider
    return ref_provider.is_bucket(param_ref)

def is_base_param(param_ref: str) -> bool:
    ref_provider = configure.infer_context().provider_provider.ref_store_provider
    return ref_provider.exists(param_ref)

def get_param_by_ref(param_ref: str) -> str:
    if param_ref not in PARAM_MAP:
        ref_provider = configure.infer_context().provider_provider.ref_store_provider
        w = Text(ref_provider.get_default_value(param_ref))
        PARAM_MAP[param_ref] = w
    return PARAM_MAP[param_ref]

def get_filename_by_ref(param_ref: str) -> str:
    ref_provider = configure.infer_context().provider_provider.ref_store_provider
    return list(ref_provider.get_nav_breadcrumbs(param_ref).values())[0]


class ParamBucket:
    def __init__(self, name_parts: list):
        '''
        List of strings that represent the name of the parameter.
        For example, 'P.foo.bar' would be ['foo', 'bar']
        '''
        self.name_parts = name_parts

    def __getattr__(self, name):
        new_name = self.__as_ref(name)
        if is_bucket(new_name):
            return ParamBucket(self.name_parts + [name])
        if is_base_param(new_name):
            return get_param_by_ref(new_name)
        want_file = get_filename_by_ref(new_name)
        explainers.missing_file_ref(new_name, want_file)

    def __as_ref(self, subname: str = None):
        if subname is None:
            return '.'.join(self.name_parts)
        return '.'.join(self.name_parts + [subname])
        
P = ParamBucket(['P'])
