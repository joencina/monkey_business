from market_project.tests import factories
from pytest_factoryboy import register

register(factories.ProductFactory)
register(factories.ProductFactory, "second_product")
register(factories.OrderFactory)