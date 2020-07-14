from django.db import models
from django.utils import timezone


class ProductOrder(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    products_on_order = models.IntegerField(default=0)


class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(decimal_places=2, max_digits=9)
    description = models.CharField(max_length=200, default='')
    featured = models.BooleanField(default=False)
    image = models.ImageField()

    def __str__(self):
        return self.name


class UserID(models.Model):
    user_id = models.CharField(max_length=200)


class Order(models.Model):
    user_id = models.OneToOneField(UserID, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=200)
    customer_address = models.CharField(max_length=200)
    customer_email = models.EmailField(max_length=200, null=True)
    order_date = models.DateTimeField()
    message = models.CharField(null=True, max_length=5000)
    products = models.ManyToManyField('Product', related_name='products')
    total = models.IntegerField(default=0)

    def __str__(self):
        return str(f"{self.customer_name}, Total: {self.total}, on {self.order_date.strftime('%m/%d/%Y')}")



