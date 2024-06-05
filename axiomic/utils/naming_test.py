
import axiomic.utils.naming as naming
import axiomic.errors as errors

Name = naming.Name

def test_full_names():
    assert naming.is_full_name('Bucket:Dir:Base')
    assert naming.is_full_name('Bucket-_012:D02-_ir:B12-_ase')
    assert not naming.is_full_name('_Bucket-_012:D02-_ir:B12-_ase')
    assert not naming.is_full_name('-Bucket-_012:D02-_ir:B12-_ase')
    assert not naming.is_full_name('0Bucket-_012:D02-_ir:B12-_ase')
    assert not naming.is_full_name(' 0Bucket-_012:D02-_ir:B12-_ase')
    assert not naming.is_full_name('Bucket:D ir:Base')
    assert not naming.is_full_name('Bucket:D@ir:Base')


def test_refernce_types():
    assert Name('p/Bucket:Dir:Base').type_name == 'p'
    assert Name('var/Bucket:Dir:Base').type_name == 'var'
    assert Name('pair/Bucket:Dir:Base').type_name == 'pair'
    assert Name('pair/Base').type_name == 'pair'



def test_get_embedded_refs():
    story = '''
Hello there. {p/foo} is here. and {p/buck:di:name} wow! 
And {p/uh:oh} is also there.
    '''
    hits = naming.get_imbedded_refs(story)
    assert hits == ['p/foo', 'p/buck:di:name', 'p/uh:oh']


