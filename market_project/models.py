from django.db import models


# DONE: Session users.
# TODO: Remember .gitignore

# DONE: get rid of line 12 after refactoring
class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.IntegerField()
    description = models.CharField(max_length=200, default='')
    featured = models.BooleanField(default=False)
    # orders = models.ManyToManyField('Order', related_name='orders', through='ProductOrder')
    image = models.ImageField()

    def __str__(self):
        return self.name


class Order(models.Model):
    user_id = models.CharField(max_length=200, primary_key=True)
    customer_name = models.CharField(max_length=200)
    customer_address = models.CharField(max_length=200)
    customer_email = models.CharField(max_length=200, null=True)
    order_date = models.DateTimeField()
    message = models.CharField(null=True, max_length=5000)
    products = models.ManyToManyField('Product', related_name='products', through='ProductOrder')
    total = models.IntegerField(default=0)

    def __str__(self):
        return str(self.order_date)


# NOT DONE: Maybe remove it
class ProductOrder(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    products_on_order = models.IntegerField(default=0)
