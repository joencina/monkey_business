from pytest import fixture
from typing import Union, Type
from market_project.tests.factories import ProductFactory, OrderFactory, UserFactory
from market_project.models import Product, Order, UserID
import chromedriver_autoinstaller
from selenium import webdriver

chromedriver_autoinstaller.install()


@fixture(scope='session')
def django_db_modify_db_settings():
    pass


@fixture
def driver(request):
    options = webdriver.ChromeOptions()
    browser = webdriver.Chrome(chrome_options=options)
    yield browser


@fixture
def product() -> Product:
    return ProductFactory()


@fixture
def featured_product() -> Product:
    return ProductFactory(featured=True)


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


@fixture
def user() -> UserID:
    return UserFactory()


@fixture
def user_factory() -> Union[Type[UserID], Type[UserFactory]]:
    return UserFactory
