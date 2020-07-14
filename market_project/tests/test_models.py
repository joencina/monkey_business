from decimal import Decimal

import pytest

pytestmark = pytest.mark.django_db


def test_product_fixture(product):
    assert str(product) == product.name
    assert isinstance(product.price, Decimal)
    assert product.featured is False


def test_second_product_fixture(second_product):
    assert str(second_product) == second_product.name
    assert isinstance(second_product.price, Decimal)
    assert not second_product.featured


def test_order_creation_and_deletion(order, product, second_product):
    order.products.add(product, second_product)
    assert order.products.count() == 2
    assert order.products.all()[0] == product
    assert order.products.all()[1] == second_product
    order.products.remove(product)
    assert order.products.count() == 1
    order.products.remove(second_product)
    assert order.products.count() == 0
