from market_project.forms import CheckoutForm


def test_form_valid():
    form = CheckoutForm({'name': 'A', 'address': 'A', 'email': 'example@example.com', 'message': 'A'})
    assert form.is_valid()


def test_name_invalid():
    form = CheckoutForm({'name': '', 'address': 'A', 'email': 'example@example.com', 'message': 'A'})
    assert not form.is_valid()


def test_address_invalid():
    form = CheckoutForm({'name': 'A', 'address': '', 'email': 'example@example.com', 'message': 'A'})
    assert not form.is_valid()


def test_email_invalid():
    form = CheckoutForm({'name': 'A', 'address': 'A', 'email': 'example@example.', 'message': 'A'})
    assert not form.is_valid()


def test_message_not_required():
    form = CheckoutForm({'name': 'A', 'address': 'A', 'email': 'example@example.com', 'message': ''})
    assert form.is_valid()
