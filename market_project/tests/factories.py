import factory
import factory.fuzzy
from django.contrib.auth.models import User

from market_project import models
from market_project.forms import CheckoutForm


class ProductFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Product

    name = factory.Sequence(lambda n: f"Product {n}")
    price = factory.fuzzy.FuzzyDecimal(1.00, 99.99)
    description = factory.Faker("sentence")
    image = factory.Faker("file_path")


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.UserID

    user_id = factory.Faker("bothify", text="#?" * 16)


class OrderFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Order

    user_id = factory.SubFactory(UserFactory)
    customer_name = factory.Faker("name")
    customer_address = factory.Faker("address")
    customer_email = factory.Faker("email")
    order_date = factory.Faker("date_object")
    message = factory.Faker("sentence")
