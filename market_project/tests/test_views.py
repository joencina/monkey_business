import pytest
from django.core import mail
from django.urls import reverse, reverse_lazy


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
def test_order_str(order):
    assert order.customer_name in str(order)


@pytest.mark.parametrize("num_product, num_second_product", [(5, 4)])
@pytest.mark.django_db
def test_shopping_cart_total_changes_appropriately(client, product, second_product, num_product, num_second_product):
    """
    Functional test to check if the shopping cart's total count changes appropriately with operations
    """

    # Starts with empty cart
    url = reverse('index')
    response = client.get(url)
    assert response.context['total'] == 0

    # Test adding products
    url_add_product = reverse('add_to_cart', args=(product.id,))
    for num in range(1, num_product + 1):
        client.get(url_add_product)
        assert client.get(url).context['total'] == num

    # Test removing all but 2 of them
    url_remove_product = reverse('remove_one_from_cart', args=(product.id,))
    for num in range(num_product - 1, 1, -1):
        client.get(url_remove_product)
        assert client.get(url).context['total'] == num
    assert client.get(url).context['total'] == 2

    # Test adding second_products
    url_add_second_product = reverse('add_to_cart', args=(second_product.id,))
    for num in range(3, num_second_product + 3):
        client.get(url_add_second_product)
        assert client.get(url).context['total'] == num

    # Test deleting products
    client.get(reverse('delete_product_from_cart', args=(product.id,)))
    assert client.get(url).context['total'] == num_second_product

    # Test deleting second_products
    client.get(reverse('delete_product_from_cart', args=(second_product.id,)))
    assert client.get(url).context['total'] == 0


@pytest.mark.parametrize("num_product, num_second_product", [(5, 4)])
@pytest.mark.django_db
def test_checkout(client, product, second_product, num_product, num_second_product, order):
    url = reverse('index')
    # Adds products
    url_add_product = reverse('add_to_cart', args=(product.id,))
    for num in range(num_product):
        client.get(url_add_product)
    assert client.get(url).context['total'] == num_product
    url_add_second_product = reverse('add_to_cart', args=(second_product.id,))
    for num in range(num_second_product):
        client.get(url_add_second_product)
    assert client.get(url).context['total'] == num_product + num_second_product
    # Checkout
    total_price = product.price*num_product + second_product.price*num_second_product
    data = {'name': order.customer_name, 'email': order.customer_email,
            'address': order.customer_address, 'message': order.message}
    client.post(reverse_lazy('checkout'), data)
    # Test email is in outbox with the right parameters
    assert len(mail.outbox) == 2
    assert mail.outbox[0].subject == f'Order received from {order.customer_name}'
    assert f"${total_price}" in mail.outbox[0].body
    assert f"shipped to {order.customer_address}" in mail.outbox[0].body
    # Test cart is empty
    assert client.get(url).context['total'] == 0
