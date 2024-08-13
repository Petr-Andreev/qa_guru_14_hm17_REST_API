import requests

endpoint_post_user = '/api/users'
endpoint_update_user = '/api/users/'

payload_post = {
    "name": "morpheus",
    "job": "leader"
}

payload_put = {
    "name": "morpheus",
    "job": "zion resident"
}

payload_patch = {
    "job": "zion resident"
}

update_job = 'zion resident'


def test_put_user(base_url):
    response = requests.post(base_url + endpoint_post_user, data=payload_post)
    body = response.json()
    update = requests.put(base_url + endpoint_update_user + body['id'], data=payload_put)
    assert update.status_code == 200
    assert update.json()['job'] == update_job


def test_patch_user_job(base_url):
    response = requests.post(base_url + endpoint_post_user, data=payload_post)
    body = response.json()
    update = requests.patch(base_url + endpoint_update_user + body['id'], data=payload_patch)
    assert update.status_code == 200
    assert update.json()['job'] == update_job
