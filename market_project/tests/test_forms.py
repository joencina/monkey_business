import pytest

from market_project.forms import CheckoutForm


@pytest.mark.django_db()
def test_form_valid():
    form = CheckoutForm({'name': 'A', 'address': 'A', 'email': 'example@example.com', 'message': 'A'})
    assert form.is_valid()


@pytest.mark.django_db()
def test_name_invalid():
    form = CheckoutForm({'name': '', 'address': 'A', 'email': 'example@example.com', 'message': 'A'})
    assert form.is_valid() is False


@pytest.mark.django_db()
def test_address_invalid():
    form = CheckoutForm({'name': 'A', 'address': '', 'email': 'example@example.com', 'message': 'A'})
    assert form.is_valid() is False


@pytest.mark.django_db()
def test_email_invalid():
    form = CheckoutForm({'name': 'A', 'address': 'A', 'email': 'example@example.', 'message': 'A'})
    assert form.is_valid() is False


@pytest.mark.django_db()
def test_message_not_required():
    form = CheckoutForm({'name': 'A', 'address': 'A', 'email': 'example@example.com', 'message': ''})
    assert form.is_valid()
