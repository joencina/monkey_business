from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from market_project import settings
from market_project.views import Index, SingleProduct

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Index.as_view(), name='index'),
    path('product/<int:pk>', SingleProduct.as_view(), name='single_product')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
