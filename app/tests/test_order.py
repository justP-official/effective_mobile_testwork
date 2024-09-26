from http import HTTPStatus

import pytest

# @pytest.mark.parametrize('')
def test_create_order(test_client, order_payload, product_payload):
    response = test_client.post('/products', json=product_payload)

    response = test_client.post('/orders', json=order_payload)

    response_json = response.json()

    assert response.status_code == HTTPStatus.OK
    
    assert response_json['status'] == order_payload['status']

def test_get_orders(test_client, order_payload, product_payload):
    response = test_client.post('/products', json=product_payload)

    response = test_client.post('/orders', json=order_payload)

    response = test_client.get('/orders')

    response_json = response.json()

    assert response.status_code == HTTPStatus.OK
    assert len(response_json) > 0

def test_get_order(test_client, order_payload, product_payload):
    response = test_client.post('/products', json=product_payload)

    response = test_client.post('/orders', json=order_payload)

    assert response.status_code == HTTPStatus.OK
    
    response = test_client.get(f'/orders/{order_payload["id"]}')

    response_json = response.json()

    assert response.status_code == HTTPStatus.OK
    assert response_json['id'] == order_payload['id']

def test_update_order_status(test_client, order_payload, order_update_status_payload, product_payload):
    response = test_client.post('/products', json=product_payload)

    response = test_client.post('/orders', json=order_payload)

    assert response.status_code == HTTPStatus.OK

    response = test_client.patch(f'/orders/{order_payload["id"]}/status', json=order_update_status_payload)

    response_json = response.json()

    print(response_json)

    assert response.status_code == HTTPStatus.OK

    assert response_json['status'] == order_update_status_payload['status']
    
    
