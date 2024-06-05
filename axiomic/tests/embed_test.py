
import axiomic 


def test_embedding():
    dog = axiomic.Text('I own a dog').embed().value()
    cat = axiomic.Text('I own a cat').embed().value()
    assert dog.cosine_similarity(cat) > 0.5
