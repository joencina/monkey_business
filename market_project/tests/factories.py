import factory
from django.contrib.auth.models import User

from market_project import models
from market_project.forms import CheckoutForm


class ProductFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Product

    name = factory.Sequence(lambda n: f"Product {n}")
    price = factory.Sequence(lambda n: n + 1)
    description = factory.Faker("sentence")
    image = factory.Faker("file_path")


class OrderFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Order

    user_id = factory.Faker("bothify", text="#?" * 16)
    customer_name = factory.Faker("name")
    customer_address = factory.Faker("address")
    customer_email = factory.Faker("email")
    order_date = factory.Faker("date_object")
    message = factory.Faker("sentence")


# class ProductOrderFactory(factory.DjangoModelFactory):
#     class Meta:
#         model = models.ProductOrder
#
#     order = factory.SubFactory(OrderFactory)
#     product = factory.SubFactory(ProductFactory)
#     products_on_order = 0
#
#
# class OrderWithProductFactory(OrderFactory):
#     membership = factory.RelatedFactory(
#         ProductOrderFactory,
#         factory_related_name='order',
#     )
