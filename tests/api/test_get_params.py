import json
from resource import path

import requests
from jsonschema.validators import validate

endpoint = '/api/users'
endpoint_user = '/api/users/2'
endpoint_user_not_found = '/api/users/123321'
endpoint_list_resource = '/api/unknown'
endpoint_single_resource = '/api/unknown/1'
endpoint_single_resource_not_found = '/api/unknown/123321'
params = 'page=2'
support_text = 'To keep ReqRes free, contributions towards server costs are appreciated!'
support_url = 'https://reqres.in/#support-heading'
schema_list_users = path('list_users_schema.json')
schema_single_user = path('single_user_schema.json')
schema_list_resource = path('list_resource_schema.json')
schema_single_resource = path('single_resource_schema.json')


def test_get_list_users(base_url):
    response = requests.get(base_url + endpoint, params=params)
    body = response.json()
    assert response.status_code == 200
    assert body['page'] == 2
    assert body['per_page'] == 6
    assert body['total'] == 12
    assert len(body['data']) == body['per_page']
    assert body['data'] != []

    with open(schema_list_users) as f:
        validate(body, schema=json.loads(f.read()))


def test_get_single_user(base_url):
    id_user = 2
    email = "janet.weaver@reqres.in"
    first_name = "Janet"
    last_name = "Weaver"
    avatar = "https://reqres.in/img/faces/2-image.jpg"

    response = requests.get(base_url + endpoint_user)
    body = response.json()
    assert response.status_code == 200
    assert body['data']["id"] == id_user
    assert body['data']["email"] == email
    assert body['data']["first_name"] == first_name
    assert body['data']["last_name"] == last_name
    assert body['data']["avatar"] == avatar

    with open(schema_single_user) as f:
        validate(body, schema=json.loads(f.read()))


def test_get_single_user_not_found(base_url):
    response = requests.get(base_url + endpoint_user_not_found)
    body = response.json()
    assert response.status_code == 404
    assert body == {}


def test_get_list_resource(base_url):
    response = requests.get(base_url + endpoint_list_resource)
    body = response.json()
    assert response.status_code == 200
    assert body['page'] == 1
    assert body['per_page'] == 6
    assert body['data'] != []
    assert len(body['data']) == body['per_page']
    assert body['total'] == 12
    assert body['total_pages'] == 2
    assert body['support']['text'] == support_text

    with open(schema_list_resource) as f:
        validate(body, schema=json.loads(f.read()))


def test_get_single_resource(base_url):
    data = {
        "id": 1,
        "name": "cerulean",
        "year": 2000,
        "color": "#98B2D1",
        "pantone_value": "15-4020"
    }
    support = {
        "url": support_url,
        "text": support_text
    }

    response = requests.get(base_url + endpoint_single_resource)
    body = response.json()
    assert response.status_code == 200
    assert body['data'] == data
    assert body['support'] == support

    with open(schema_single_resource) as f:
        validate(body, schema=json.loads(f.read()))


def test_get_single_resource_not_found(base_url):
    response = requests.get(base_url + endpoint_single_resource_not_found)
    body = response.json()
    assert response.status_code == 404
    assert body == {}
