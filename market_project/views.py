import os

from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.datetime_safe import datetime
from django.views.generic import ListView, DetailView, FormView
from django.views.generic.base import ContextMixin, TemplateView
from strgen import StringGenerator

from market_project.forms import CheckoutForm
from market_project.models import Product, Order, UserID, ProductOrder


def get_order(request) -> Order:
    session = request.session
    session['user_id'] = session.get('user_id', StringGenerator('[\w\p\d]{32}').render())
    session.set_expiry(0)
    user_id, created = UserID.objects.get_or_create(user_id=session['user_id'])
    order, created = Order.objects.get_or_create(user_id=user_id,
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
        context['products'] = order.products.all()
        total = 0
        for product in order.products.all():
            total += ProductOrder.objects.get(order=order, product=product).products_on_order
        context['total'] = total

        return context


class Index(ListView, CartMixin):
    model = Product
    template_name = "index.html"

    def get_queryset(self):
        return Product.objects.filter(featured=True)


class Shop(ListView, CartMixin):
    model = Product
    template_name = "shop.html"
    paginate_by = 9


class Cart(CartMixin, ListView):
    model = Order
    template_name = "cart.html"

    def get_context_data(self, **kwargs):  # This block of code is repeated
        context = super().get_context_data(**kwargs)
        order = get_order(self.request)
        total_price = 0
        for product in context['products']:
            po = ProductOrder.objects.get(order=order, product=product)
            product.products_on_order = po.products_on_order  # Quantity of each product
            product.subtotal = product.products_on_order * product.price  # Subtotal for each product in cart
            total_price += product.subtotal
        context['total_price'] = total_price
        return context


#
#
class Checkout(FormView, Cart):
    form_class = CheckoutForm
    template_name = 'checkout.html'

    def form_valid(self, form):
        order = get_order(self.request)
        order_products = order.products.all()
        total_price = 0
        for product in order_products:
            po = ProductOrder.objects.get(order=order, product=product)
            product.products_on_order = po.products_on_order
            product.subtotal = po.products_on_order * product.price
            total_price += product.subtotal

        params = {'name': self.request.POST.get('name'),
                  'address': self.request.POST.get('address'),
                  'email': self.request.POST.get('email'),
                  'message': self.request.POST.get('message'),
                  'products': order_products,
                  'total_price': total_price}

        send_mail(f'Order received from {params["name"]}',
                  render_to_string('email_template.txt', params),
                  os.getenv("NO_REPLY_EMAIL"),
                  [os.getenv("STORE_OWNER_EMAIL")],
                  html_message=(render_to_string('email_template.html', params)),
                  fail_silently=False)

        send_mail(f'Congratulations! We received your order.',
                  render_to_string('email_costumer.txt', params),
                  os.getenv("NO_REPLY_EMAIL"),
                  [f"{params['email']}"],
                  html_message=(render_to_string('email_costumer.html', params)),
                  fail_silently=False)

        order.order_date = timezone.now()
        order.completed = True
        order.save()
        self.request.session['user_id'] = StringGenerator('[\w\p\d]{32}').render()

        return HttpResponseRedirect(reverse_lazy('thank_you'))


class ThankYou(TemplateView):
    template_name = 'thank_you.html'


class SingleProduct(DetailView, CartMixin):
    model = Product
    template_name = 'product.html'


def add_to_cart(request, pk):
    order = get_order(request)
    po, _ = ProductOrder.objects.get_or_create(order=order, product_id=pk)
    po.products_on_order += 1
    if not order.products.filter(pk=pk):
        product = get_object_or_404(Product, id=pk)
        order.products.add(product)
    po.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def remove_one_from_cart(request, pk):
    po = ProductOrder.objects.get(order=(get_order(request)), product_id=pk)
    if po.products_on_order:
        po.products_on_order -= 1
        po.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def delete_product_from_cart(request, pk):
    order = get_order(request)
    product = get_object_or_404(Product, id=pk)
    order.products.remove(product)
    po = get_object_or_404(ProductOrder, order=get_order(request), product_id=pk)
    po.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
