import pytest


from pytest import fixture
from typing import Union, Type
from market_project.tests.factories import ProductFactory, OrderFactory
from market_project.models import Product, Order


@fixture
def product() -> Product:
    return ProductFactory()


@fixture
def second_product() -> Product:
    return ProductFactory()


@fixture
def product_factory() -> Union[Type[Product], Type[ProductFactory]]:
    return ProductFactory


@fixture
def order() -> Order:
    return OrderFactory()


@fixture
def order_factory() -> Union[Type[Order], Type[OrderFactory]]:
    return OrderFactory
