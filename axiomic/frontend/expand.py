


import axiomic.models as models

import axiomic.errors as errors

import axiomic.utils.paramtool as paramtool
import weakref
import re





'''
This implements recursive parameter expansion through subsitution of a string.

For example:
"My {P.foo}" -> "My {P.whiz} and {P.bang}" -> "My cat and dog"

This is done through creating texts for each component, and then building a tree which is
seralized into the string.

"My {P.foo}" -> "My {textref-12345}"
and textref-12345 =  "{weaveref-22345} and {weaveref-32345}"
textref-22345 = "cat
textref-32345 = "dog"
'''

ACTIVE_textS = weakref.WeakValueDictionary()
text_REF_REGEX = re.compile(r'{(weaveref_0x[a-z0-9]+)}')


def magic_name(w):
    return 'textref_' + hex(id(w))


def list_text_magic_names(text: str) -> list:
    return text_REF_REGEX.findall(text)


def get_param_by_ref(param_ref: str) -> str:
    ref_provider = models.infer_context().provider_provider.ref_store_provider
    return ref_provider.get_default_value(param_ref)


def track_text(w):
    ACTIVE_textS[magic_name(w)] = w


def text_format_place_holder(w):
    return f'{{{magic_name(w)}}}'


def swap_param_for_text(text: str, param_name, w) -> str:
    text_magic_name = magic_name(w)
    p_format_name = f'{{{param_name}}}'
    return text.replace(p_format_name, f'{{{text_magic_name}}}')

def get_active_text(weave_magic_name: str):
    if text_magic_name not in ACTIVE_WEAVES:
        raise errors.textError(f'(Internal Error - please report) No such active weave: {weave_magic_name}')
    return ACTIVE_textS[weave_magic_name]


def text_needs_expand(text: str) -> bool:
    params_mentioned = paramtool.get_all_imbedded_params(text)
    if params_mentioned:
        return True

    texts_mentioned = list_text_magic_names(text)
    if texts_mentioned:
        return True

    return False


def recur_build_wave_with_subs(text: str, Text_: callable):
    '''
    This will build out a text graph while subsitute param values.
    '''
    params_mentioned = paramtool.get_all_imbedded_params(text)
    formats = {}
    for param_name in params_mentioned:
        param_text = get_param_by_ref(param_name)
        param_as_text = recur_build_wave_with_subs(param_text, Text_)
        text = swap_param_for_text(text, param_name, param_as_text)
        formats[magic_name(param_as_text)] = param_as_text

    for text_magic_name in list_text_magic_names(text):
        w = get_active_text(weave_magic_name)
        formats[text_magic_name] = w

    if not formats:
        w = Text_(text)
        track_text(w)
        return w


    # We need to find text refs as well
    w = Text_(text, autoexpand=False)
    track_text(w)
    w = w.format(**formats)
    track_text(w)
    return w
