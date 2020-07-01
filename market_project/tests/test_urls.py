from django import urls

def test_index(client):
    """
    Verifies that home page renders correctly
    """
    url = urls.reverse('index')
    response = client.get(url)
    print(response)
    assert response.status_code == 200
    assert b'Hey' in response.content
