from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils.datetime_safe import datetime
from django.views.generic import ListView, DetailView
from django.views.generic.base import ContextMixin
from strgen import StringGenerator

from market_project.models import Product, Order, ProductOrder


def get_order(request) -> Order:
    session = request.session
    session['user_id'] = session.get('user_id', StringGenerator('[\w\p\d]{32}').render())
    session.set_expiry(0)
    order, created = Order.objects.get_or_create(user_id=session['user_id'],
                                                 defaults={'customer_name': '',
                                                           'customer_address': '',
                                                           'order_date': datetime.now()})
    return order


class CartMixin(ContextMixin):
    def __init__(self):
        self.request = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = get_order(self.request)
        order_products = order.products.all()
        context['total'] = order.total
        context['products'] = order_products
        return context


class Index(ListView, CartMixin):
    model = Product
    template_name = "index.html"

    def get_queryset(self):
        return Product.objects.filter(featured=True)


class Shop(ListView, CartMixin):
    model = Product
    template_name = "shop.html"


class Cart(ListView, CartMixin):
    model = ProductOrder
    template_name = "cart.html"

    def get_queryset(self):
        order = get_order(self.request)
        return ProductOrder.objects.filter(order__user_id=order.user_id)


class SingleProduct(DetailView, CartMixin):
    model = Product
    template_name = 'product.html'


def cart_operations(request, pk, operation):
    product = get_object_or_404(Product, id=pk)
    order = get_order(request)
    po, po_created = ProductOrder.objects.get_or_create(product=product, order=order)
    if operation == "add":
        po.products_on_order += 1
        order.total += 1
        po.save()
    elif operation == "remove":
        po.products_on_order -= 1
        order.total -= 1
        po.save()
    elif operation == "delete":
        order.total -= po.products_on_order
        po.delete()
    order.save()


def add_to_cart(request, pk):
    cart_operations(request, pk, operation="add")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def remove_one_from_cart(request, pk):
    cart_operations(request, pk, operation="remove")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def delete_product_from_cart(request, pk):
    cart_operations(request, pk, operation="delete")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
