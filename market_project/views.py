import os

from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.datetime_safe import datetime
from django.views.generic import ListView, DetailView, FormView
from django.views.generic.base import ContextMixin, TemplateView
from strgen import StringGenerator

from market_project.forms import CheckoutForm
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
    paginate_by = 9


class Cart(ListView, CartMixin):
    model = ProductOrder
    template_name = "cart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = get_order(self.request)
        order_products = order.products.all()
        context['total'] = order.total
        context['products'] = order_products

        total_price = 0
        for product in order_products:
            po = ProductOrder.objects.get(order=order, product=product)
            product.products_on_order = po.products_on_order
            product.subtotal = po.products_on_order * product.price
            total_price += product.subtotal
        context['total_price'] = total_price
        return context


class Checkout(FormView, Cart):
    form_class = CheckoutForm
    template_name = 'checkout.html'

    def form_valid(self, form):
        order = get_order(self.request)
        order_products = order.products.all()

        name = self.request.POST.get('name')
        address = self.request.POST.get('address')
        email = self.request.POST.get('email')
        message = self.request.POST.get('message')
        content = f"{name} just made an order to be shipped to {address} consisting of the following:\n"
        html = f"""<strong>{name}</strong> just made an order to be shipped to
                     <strong>{address}</strong> consisting of the following:
                    <h3>Billing details</h3>
                    <table><thead><th style='text-align:left'>Product</th>
                    <th style='text-align:center'>Total</th></thead><tbody>"""
        total_price = 0
        for product in order_products:
            po = ProductOrder.objects.get(order=order, product=product)
            product.subtotal = po.products_on_order * product.price
            total_price += product.subtotal
            content += f"{po.products_on_order} x {product.name} (at ${product.price} each) = ${product.subtotal}\n"
            html += f"""<tr><td>{product.name}<strong class="mx-2"> &times; </strong>{po.products_on_order}</td>
                        <td>${product.subtotal}</td></tr>"""
            cart_operations(self.request, product.pk, operation="delete")
        content += f"Total: ${total_price}"

        html += f"""<tr><td class="text-black font-weight-bold"><strong>Order Total</strong></td>
                    <td class="text-black font-weight-bold"><strong>${total_price}</strong></td></tr></tbody></table>"""
        if message:
            html += f"<h3>Additional comments:</h3><p>{message}</p>"
            content += f"\n\nAdditional comments:\n{message}"

        # Send email to store owner

        send_mail(f'Order received from {name}', content, 'noreply@encina.xyz', [os.getenv("STORE_OWNER_EMAIL")],
                  html_message=html, fail_silently=False)

        # Send email to costumer
        html_costumer = html.replace(f"<strong>{name}</strong>", "You")
        content_client = content.replace(f"{name}", "You")

        send_mail(f'Congratulations! We received your order.', content_client, 'noreply@encina.xyz', [f"{email}"],
                  html_message=html_costumer, fail_silently=False)

        return HttpResponseRedirect(reverse_lazy('thank_you'))


class ThankYou(TemplateView):
    template_name = 'thank_you.html'


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
