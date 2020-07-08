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
def test_shopping_cart_total_changes_appropriately(client, product):
    url = reverse('single_product', args=(product.id,))
    response = client.get(url)
    assert response.context['total'] == 0

    # Test adding 5 products
    url2 = reverse('add_to_cart', args=(product.id,))
    for num in range(1, 6):
        client.get(url2)
        response3 = client.get(url)
        assert response3.context['total'] == num

    # Test removing 2 of them
    url3 = reverse('remove_one_from_cart', args=(product.id,))
    for num in range(4, 2, -1):
        client.get(url3)
        response3 = client.get(url)
        assert response3.context['total'] == num

    # Test deleting product
    client.get(reverse('delete_product_from_cart', args=(product.id,)))
    response4 = client.get(url)
    assert response4.context['total'] == 0
