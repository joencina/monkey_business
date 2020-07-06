from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.datetime_safe import datetime
from django.views.generic import ListView, DetailView
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


class Index(ListView):
    model = Product
    template_name = "index.html"

    def get_queryset(self):
        return Product.objects.filter(featured=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = get_order(self.request)
        context['total'] = order.total
        return context


class SingleProduct(DetailView):
    model = Product
    template_name = 'product.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = get_order(self.request)
        context['total'] = order.total
        print(order.total)
        return context


def add_to_cart(request, pk):
    product = get_object_or_404(Product, id=pk)
    order = get_order(request)
    po, po_created = ProductOrder.objects.get_or_create(product=product, order=order)
    if not po_created:
        # print(po.products_on_order)
        po.products_on_order += 1
        po.save()
    order.total += 1
    order.save()
    return HttpResponseRedirect(reverse('single_product', kwargs={'pk': pk}))
