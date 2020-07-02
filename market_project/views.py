from django.views.generic import ListView, DetailView

from market_project.models import Product


class Index(ListView):
    model = Product
    template_name = "index.html"

    def get_queryset(self):
        return Product.objects.filter(featured=True)


class SingleProduct(DetailView):
    model = Product
    template_name = 'product.html'
