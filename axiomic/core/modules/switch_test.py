

import axiomic.core.modules as modules


def test_basic_switch():

    EXAMPLES = [
        ('I need help with the product I bought', '"SUPPORT"'),
        ('It is not working.', '"SUPPORT"'),
        ('I want to buy a product', '"SALES"'),
        ('I just bought a product and I need help.', '"SALES"'),
        ('I need a refund.', '"SALES"'),
        ('I do not like you. Go away.', '"COMPLAINT"')
    ]
    switch = knits.Switch(EXAMPLES)
    assert '"SUPPORT"' == switch.infer('I just bought a product and I need help.').value()
