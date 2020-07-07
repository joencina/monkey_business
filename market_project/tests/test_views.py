import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_total_in_index_context(client):
    url = reverse('index')
    response = client.get(url)
    assert response.context['total'] is not None


@pytest.mark.django_db
def test_total_in_single_product_context(client, product):
    url = reverse('single_product', args=(product.id,))
    response = client.get(url)
    assert response.context['total'] is not None


@pytest.mark.django_db
def test_adding_product_to_cart(client, product):
    url = reverse('single_product', args=(product.id,))
    response = client.get(url)
    assert response.context['total'] == 0
    url2 = reverse('add_to_cart', args=(product.id,))
    for num in range(1, 5):
        client.get(url2)
        response3 = client.get(url)
        assert response3.context['total'] == num
