import pytest
from django.utils.datetime_safe import datetime

from market_project.models import Product, Order, ProductOrder

@pytest.fixture
def product():
    return Product.objects.create(name='Test Product', price=10, image='', description='')
@pytest.fixture
def second_product():
    return Product.objects.create(name='Other Product', price=5, image='', description='')

@pytest.fixture
def order():
    return Order.objects.create(customer_name='Foo', customer_address='Bar', order_date=datetime.now())

@pytest.mark.django_db
def test_product_fixture(product):
    assert str(product) == product.name
    assert product.price == 10
    assert type(product.price) == int
    assert product.featured == False


@pytest.mark.django_db
def test_second_product_fixture(second_product):
    assert str(second_product) == second_product.name
    assert second_product.price == 5
    assert type(second_product.price) == int
    assert second_product.featured == False

@pytest.mark.django_db
def test_order_info(order):
    assert order.customer_name == 'Foo'
    assert order.customer_address == 'Bar'
    assert str(order) == str(order.order_date)

@pytest.mark.django_db
def test_order_creation(order, product, second_product):
    ProductOrder(order=order, product=product).save()
    ProductOrder(order=order, product=second_product).save()
    assert order.products.count() == 2
    assert order.products.all()[0] == product
    assert order.products.all()[1] == second_product