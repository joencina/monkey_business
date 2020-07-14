from decimal import Decimal

import pytest
from market_project.models import ProductOrder

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
    po = ProductOrder(order=order, product=product)
    po.save()
    po2 = ProductOrder(order=order, product=second_product)
    po2.save()
    assert order.products.count() == 2
    assert order.products.all()[0] == product
    assert order.products.all()[1] == second_product
    po.delete()
    assert order.products.count() == 1
    po2.delete()
    assert order.products.count() == 0
