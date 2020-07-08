from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from market_project import settings
from market_project import views

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', views.Index.as_view(), name='index'),
                  path('product/<int:pk>', views.SingleProduct.as_view(), name='single_product'),
                  path('add/<int:pk>', views.add_to_cart, name='add_to_cart'),
                  path('remove/<int:pk>', views.remove_one_from_cart, name='remove_one_from_cart'),
                  path('delete/<int:pk>', views.delete_product_from_cart, name='delete_product_from_cart'),

                  path('shop', views.Shop.as_view(), name='shop'),
                  path('cart', views.Cart.as_view(), name='cart'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
