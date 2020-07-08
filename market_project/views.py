from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.datetime_safe import datetime
from django.views import View
from django.views.generic import ListView, DetailView
from django.views.generic.base import ContextMixin
from strgen import StringGenerator

from market_project.models import Product, Order, ProductOrder


def get_order(request):
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
        context['total'] = order.total
        return context


class Index(ListView, CartMixin):
    model = Product
    template_name = "index.html"

    def get_queryset(self):
        return Product.objects.filter(featured=True)


class Shop(ListView, CartMixin):
    model = Product
    template_name = "shop.html"


class Cart(ListView):
    model = ProductOrder
    template_name = "cart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = get_order(self.request)
        context['total'] = order.total
        context['products'] = order.products.all()
        return context

    def get_queryset(self):
        order = get_order(self.request)
        return ProductOrder.objects.filter(order__user_id=order.user_id)


class SingleProduct(DetailView, CartMixin):
    model = Product
    template_name = 'product.html'


def add_to_cart(request, pk):
    product = get_object_or_404(Product, id=pk)
    order = get_order(request)
    po, po_created = ProductOrder.objects.get_or_create(product=product, order=order)
    if not po_created:
        po.products_on_order += 1
        po.save()
    order.total += 1
    order.save()
    return HttpResponseRedirect(reverse('single_product', kwargs={'pk': pk}))
