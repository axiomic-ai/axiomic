
import axiomic.utils.paramtool as paramtool 
import axiomic.errors as errors

def test_param_names():
    assert paramtool.is_param_name('P.foo')
    assert paramtool.is_param_name('P.foo.bar')
    assert not paramtool.is_param_name('P.foo.bar.')
    assert not paramtool.is_param_name('P.foo.-bar')
    assert not paramtool.is_param_name('P.foo bar')
    assert not paramtool.is_param_name('P.')
    assert not paramtool.is_param_name('P')


def test_segment_name():
    assert paramtool.segment_param_name('P.foo') == ['foo']
    assert paramtool.segment_param_name('P.foo.bar') == ['foo', 'bar']
    assert paramtool.segment_param_name('P.foo.bar.Whi8z') == ['foo', 'bar', 'Whi8z']


def test_get_imbedded_params():
    assert paramtool.get_all_imbedded_params('{P.foo}') == ['P.foo']
    assert paramtool.get_all_imbedded_params('Hello {P.foo}!') == ['P.foo']
    assert paramtool.get_all_imbedded_params('My {P.foo} is {P.bar}') == ['P.foo', 'P.bar']



