import pytest
from django import urls

from market_project.models import Product


@pytest.fixture
def product():
    return Product.objects.create(name='test', price=1, image='bread.png', description='')


@pytest.mark.django_db
def test_index(client):
    """
    Verifies that home page renders correctly
    """
    url = urls.reverse('index')
    response = client.get(url)
    assert response.status_code == 200
    assert b'Market' in response.content


@pytest.mark.django_db
def test_single_product(client, product):
    """
    Verifies that single product page renders correctly
    """
    url = urls.reverse('single_product', args=(product.id,))
    response = client.get(url)
    print(response)
    assert response.status_code == 200
