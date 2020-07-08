import pytest
from django import urls

url_list = [('index', b'Market'), ('shop', b'Shop'), ('cart', b'Cart')]


@pytest.mark.parametrize("url_name, text", url_list)
@pytest.mark.django_db
def test_list_pages(client, url_name, text):
    """
    Verifies that pages render correctly
    """
    url = urls.reverse(url_name)
    response = client.get(url)
    assert response.status_code == 200
    assert text in response.content


@pytest.mark.django_db
def test_single_product(client, product):
    """
    Verifies that the single product page renders correctly
    """
    url = urls.reverse('single_product', args=(product.id,))
    response = client.get(url)
    assert response.status_code == 200
