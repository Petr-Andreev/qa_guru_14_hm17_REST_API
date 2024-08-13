import json
from resource import path
from datetime import datetime, timedelta
import requests
from jsonschema.validators import validate

endpoint_create_user = '/api/users'
endpoint_login = '/api/login'
endpoint_register = '/api/register'
schema_login_successful = path('login_successful_schema.json')


def test_post_create_user(base_url):
    payload = {
        "name": "morpheus",
        "job": "leader"
    }
    name = 'morpheus'
    job = 'leader'
    response = requests.post(base_url + endpoint_create_user, data=payload)
    body = response.json()

    # Преобразование даты от сервера из ISO формата и коррекция времени от сервера на 3 часа
    # Преобразование даты от сервера в нужный формат
    server_datetime = datetime.fromisoformat(body['createdAt'].replace('Z', '+00:00'))
    server_datetime_corrected = server_datetime + timedelta(hours=3)
    server_time_formatted = server_datetime_corrected.strftime("%Y-%m-%d %H:%M")

    # Преобразование текущей даты и времени в нужный формат
    current_datetime = datetime.now()
    current_time_formatted = current_datetime.strftime("%Y-%m-%d %H:%M")

    assert response.status_code == 201
    assert body['name'] == name
    assert body['job'] == job
    assert body['id']
    assert server_time_formatted == current_time_formatted


def test_post_login_successful(base_url):
    payload = {
        "email": "eve.holt@reqres.in",
        "password": "cityslicka"
    }
    response = requests.post(base_url + endpoint_login, data=payload)
    body = response.json()
    assert response.status_code == 200
    assert 'token' in response.json()
    assert body['token']

    with open(schema_login_successful) as f:
        validate(body, schema=json.loads(f.read()))


def test_post_login_unsuccessful(base_url):
    payload = {
        "email": "peter@klaven"
    }
    error = 'Missing password'
    response = requests.post(base_url + endpoint_login, data=payload)
    assert response.status_code == 400
    assert response.json()['error'] == error


def test_post_register_successful(base_url):
    payload = {
        "email": "eve.holt@reqres.in",
        "password": "pistol"
    }
    response = requests.post(base_url + endpoint_register, data=payload)
    assert response.status_code == 200
    assert response.json()['id'] == 4
    assert response.json()['token']


def test_post_register_unsuccessful(base_url):
    payload = {
        "email": "abrakadabra@fife_ninja.com",
    }
    error = 'Missing password'
    response = requests.post(base_url + endpoint_register, data=payload)
    assert response.status_code == 400
    assert response.json()['error'] == error
