

import re

import axiomic.logalytics.explainers as explainers


IMPLIED_BUCKET = 'default'
IMPLIED_DIRNAME = 'default'

NAME_BASENAME_PAT = r'[a-zA-Z][a-zA-Z0-9_.-]+'
NAME_DIRNAME_PAT  = r'[a-zA-Z][a-zA-Z0-9_-]+'
NAME_BUCKET_PAT = r'[a-zA-Z][a-zA-Z0-9_-]*'

# Matches <BUCKET>:<SUBBUCKET>:<BASENAME>
FULL_NAME_REGEX = re.compile(f'^(?P<bucket>{NAME_BUCKET_PAT}):(?P<dir>{NAME_DIRNAME_PAT}):(?P<basename>{NAME_BASENAME_PAT})$')
NAME_IMPLIED_BUCKET_REGEX = re.compile(f'^(?P<dir>{NAME_DIRNAME_PAT}):(?P<basename>{NAME_BASENAME_PAT})$')
NAME_IMPLIED_DIR_REGEX = re.compile(f'^(?P<basename>{NAME_BASENAME_PAT})$')


REFERENCE_TYPES = ['p', 'var', 'pair']
REFERENCE_TYPES_OR_PAT = '|'.join(REFERENCE_TYPES)

# For example, match "param/Bucket:Dir:Base"
# FULL_REFERENCE_REGEX = re.compile(f'^(?P<type>{REFERENCE_TYPES_OR_PAT})/...
FULL_REFERENCE_REGEX = re.compile(f'^(?P<type>{REFERENCE_TYPES_OR_PAT})/(?P<bucket>{NAME_BUCKET_PAT}):(?P<dir>{NAME_DIRNAME_PAT}):(?P<basename>{NAME_BASENAME_PAT})$')
REFERENCE_IMPLIED_BUCKET_REGEX = re.compile(f'^(?P<type>{REFERENCE_TYPES_OR_PAT})/(?P<dir>{NAME_DIRNAME_PAT}):(?P<basename>{NAME_BASENAME_PAT})$')
REFERFENCE_IMPLIED_DIR_REGEX = re.compile(f'^(?P<type>{REFERENCE_TYPES_OR_PAT})/(?P<basename>{NAME_BASENAME_PAT})$')


IMMBEDDED_REF_PAT = f'{{(?P<type>{REFERENCE_TYPES_OR_PAT})/(?P<bucket>{NAME_BUCKET_PAT}:)?(?P<dir>{NAME_DIRNAME_PAT}:)?(?P<basename>{NAME_BASENAME_PAT})}}'
IMBEDDED_REF_REGEX = re.compile(IMMBEDDED_REF_PAT)


def get_imbedded_refs(text: str) -> list:
    hits = IMBEDDED_REF_REGEX.findall(text)

    l = []
    for h in hits:
        r = h[0] + '/'
        stuff = ''.join(h[1:])
        l.append(r + stuff)
    return l


def is_name(name: str) -> bool:
    if FULL_NAME_REGEX.match(name) is not None:
        return True
    
    if NAME_IMPLIED_BUCKET_REGEX.match(name) is not None:
        return True
    
    if NAME_IMPLIED_DIR_REGEX.match(name) is not None:
        return True

    return False


def convert_to_full_name(name: str) -> str:
    if m := FULL_NAME_REGEX.match(name):
        return name
    
    if m := NAME_IMPLIED_BUCKET_REGEX.match(name):
        return f'{IMPLIED_BUCKET}:{m.group("dir")}:{m.group("basename")}'

    if m := NAME_IMPLIED_DIR_REGEX.match(name):
        return f'{IMPLIED_BUCKET}:{IMPLIED_DIRNAME}:{m.group("basename")}'


def extract_name_parts(name: str) -> tuple:
    if m := FULL_NAME_REGEX.match(name):
        return m.group('bucket'), m.group('dir'), m.group('basename')
    return None, None, None


def is_full_name(name: str) -> bool:
    return FULL_NAME_REGEX.match(name) is not None


def is_full_reference_name(name: str) -> bool:
    return FULL_REFERENCE_REGEX.match(name) is not None


def is_reference_name(name: str) -> bool:
    if is_full_reference_name(name):
        return True

    if REFERENCE_IMPLIED_BUCKET_REGEX.match(name):
        return True
    
    if REFERFENCE_IMPLIED_DIR_REGEX.match(name):
        return True
    
    return False
    

def convert_to_full_reference_name(name: str) -> str:
    if m := FULL_REFERENCE_REGEX.match(name):
        return name
    
    if m := REFERENCE_IMPLIED_BUCKET_REGEX.match(name):
        return f'{m.group("type")}/{IMPLIED_BUCKET}:{m.group("dir")}:{m.group("basename")}'
    
    if m := REFERFENCE_IMPLIED_DIR_REGEX.match(name):
        return f'{m.group("type")}/{IMPLIED_BUCKET}:{IMPLIED_DIRNAME}:{m.group("basename")}'


def extract_reference_parts(name: str) -> tuple:
    if m := FULL_REFERENCE_REGEX.match(name):
        return m.group('type'), m.group('bucket'), m.group('dir'), m.group('basename')
    return None, None, None, None


class Name:
    def __init__(self, name: str):
        if isinstance(name, Name):
            self._copy(name)
            return

        if name.startswith('{') and name.endswith('}'):
            explainers.explain_wrapped_name(name)

        if name is None:
            explainers.explain_bad_name_error('<None>')

        self.original_name = name
        self.type_name = None
        self.bucket_name = None
        self.dir_name = None
        self.base_name = None
        self.is_reference = False

        if is_reference_name(name):
            self.full_name = convert_to_full_reference_name(name)
            self.type_name, self.bucket_name, self.dir_name, self.base_name = extract_reference_parts(self.full_name)
            self.is_reference = True
        elif is_name(name):
            self.full_name = convert_to_full_name(name)
            self.bucket_name, self.dir_name, self.base_name = extract_name_parts(self.full_name)
        else:
            explainers.explain_bad_name_error(name)

    def _copy(self, other):
        self.original_name = other.original_name
        self.type_name = other.type_name
        self.bucket_name = other.bucket_name
        self.dir_name = other.dir_name
        self.base_name = other.base_name
        self.is_reference = other.is_reference

    def __str__(self):
        return self.full_name


        


