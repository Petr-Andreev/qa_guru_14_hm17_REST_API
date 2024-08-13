import requests

endpoint_delete_user = '/api/users'
payload = {
    "name": "morpheus",
    "job": "leader"
}


def test_delete_user(base_url):
    response = requests.post(base_url + endpoint_delete_user, data=payload)
    body = response.json()
    delete = requests.delete(base_url + endpoint_delete_user + body['id'])
    assert delete.status_code == 204
