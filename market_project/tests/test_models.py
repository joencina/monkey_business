import pytest
from market_project.models import ProductOrder


# DONE: conftest.py
# DONE: GAE won't work. Amazon S3 for static files. Look up which one's easiest
# DONE: Check out factory boy
# DONE: After checking out the docs, look up pytest-factoryboy-fixtures

@pytest.mark.django_db
def test_product_fixture(product):
    assert str(product) == product.name
    assert type(product.price) == int
    assert product.featured is False


@pytest.mark.django_db
def test_second_product_fixture(second_product):
    assert str(second_product) == second_product.name
    assert type(second_product.price) == int
    assert second_product.featured is False


@pytest.mark.django_db
def test_order_info(order):
    assert str(order) == str(order.order_date)


@pytest.mark.django_db
def test_order_creation(order, product, second_product):
    ProductOrder(order=order, product=product).save()
    ProductOrder(order=order, product=second_product).save()
    assert order.products.count() == 2
    assert order.products.all()[0] == product
    assert order.products.all()[1] == second_product
