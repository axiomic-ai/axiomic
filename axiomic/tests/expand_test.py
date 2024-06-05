
import axiomic
import axiomic.frontend.expand as expand


class MockText:
    def __init__(self, value, autoexpand=None):
        self.value = value
    
    def format(self, **kwargs):
        return MockText(self.value.format(**kwargs))

    def __str__(self):
        return self.value


def test_basic_axomic_expand():
    mock_axomic_animal = MockText('animal')
    mock_axomic_dog = MockText('dog')
    expand.track_text(mock_axomic_animal)
    expand.track_text(mock_axomic_dog)
    magic_name_animal = expand.magic_name(mock_axomic_animal)
    magic_name_dog = expand.magic_name(mock_axomic_dog)
    text = f'My favorite {{{magic_name_animal}}} is a {{{magic_name_dog}}}'
    expanded = expand.recur_build_wave_with_subs(text, MockText)
    assert str(expanded) == 'My favorite animal is a dog'


def test_basic_parameter_expand():
    text = 'My schema is {P.core.jsonschema.boolean}'
    expanded = expand.recur_build_wave_with_subs(text, axiomic.Text)
    assert 'json-schema.org' in expanded.value()
