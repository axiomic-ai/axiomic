
from typing import List, Tuple
import yaml

import axiomic.utils.paramtool as paramtool
import axiomic.errors as errors



class ParamProvider:
    '''
    A reference store holds parameters, templates, etc. and information about them.
    '''
    def __init__(self, impl):
        self.impl = impl

    def exists(self, name) -> bool:
        if not paramtool.is_param_name(name):
            return False
        return self.impl.exists(name)

    def is_bucket(self, name) -> bool:
        if not paramtool.is_param_name(name):
            return False
        return self.impl.is_bucket(name)
    
    def get_nav_breadcrumbs(self, name) -> str:
        return self.impl.get_ref_nav_breadcrumbs(name)

    def get_default_value(self, name) -> str:
        if not paramtool.is_param_name(name):
            raise errors.WeaveError(f'Invalid param name: {name}')
        return self.impl.get_default_value(name)

    def get_pairs(self, name) -> List[Tuple[str, str]]:
        raw_text = self.get_default_value(name)
        a_b_pairs = yaml.safe_load(raw_text)
        l = []
        for d in a_b_pairs:
            l.append((d['A'].strip(), d['B'].strip()))
        return l
