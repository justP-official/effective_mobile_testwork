from http import HTTPStatus

def test_create_product(test_client, product_payload):
    response = test_client.post('/products', json=product_payload)

    response_json = response.json()

    assert response.status_code == HTTPStatus.OK
    assert response_json['name'] == product_payload['name']
    assert response_json['description'] == product_payload['description']
    assert response_json['price'] == str(product_payload['price'])
    assert response_json['quantity'] == product_payload['quantity']

def test_get_products(test_client, product_payload):
    response = test_client.post('/products', json=product_payload)

    response = test_client.get('/products')

    response_json = response.json()

    assert response.status_code == HTTPStatus.OK
    assert len(response_json) > 0

def test_get_product(test_client, order_payload, product_payload):
    response = test_client.post('/products', json=product_payload)

    assert response.status_code == HTTPStatus.OK
    
    response = test_client.get(f'/products/{product_payload["id"]}')

    response_json = response.json()

    assert response.status_code == HTTPStatus.OK
    assert response_json['id'] == order_payload['id']

def test_update_product(test_client, product_payload, product_update_payload):
    response = test_client.post('/products', json=product_payload)

    assert response.status_code == HTTPStatus.OK

    response = test_client.put(f'/products/{product_payload["id"]}', json=product_update_payload)

    assert response.status_code == HTTPStatus.OK

    response_json = response.json()

    assert response_json['name'] == product_update_payload['name']
    assert response_json['description'] == product_update_payload['description']
    assert response_json['price'] == str(product_update_payload['price'])
    assert response_json['quantity'] == product_update_payload['quantity']

def test_update_product(test_client, product_payload):
    response = test_client.post('/products', json=product_payload)

    assert response.status_code == HTTPStatus.OK

    response = test_client.delete(f'/products/{product_payload["id"]}')

    assert response.status_code == HTTPStatus.OK

    response = test_client.get(f'/products/{product_payload["id"]}')

    assert response.status_code == HTTPStatus.NOT_FOUND
