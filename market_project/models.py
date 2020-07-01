from django.db import models


class Orders(models.Model):
    customer_name = models.CharField(max_length=200)
    customer_address = models.CharField(max_length=200)
    order_date = models.DateTimeField()
    product = models.ManyToManyField('Products', through='OrdersProducts')


class Products(models.Model):
    name = models.CharField(max_length=200)
    price = models.IntegerField()
    units_in_stock = models.IntegerField()
    units_on_order = models.IntegerField()
    order = models.ManyToManyField('Orders', through='OrdersProducts')


class OrdersProducts(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
