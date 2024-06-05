

import axiomic.utils.pathing as pathing


def test_caller_filename():
    name = pathing.second_caller_filename()
    assert 'pytest' in name
