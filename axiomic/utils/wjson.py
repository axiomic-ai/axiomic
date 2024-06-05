
import json

'''
weave json support.
'''


def loads(s: str):
    '''
    Offer a more generous JSON parser than the built-in one.
    '''
    s = s.strip()
    return json.loads(s)