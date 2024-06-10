import re
import requests

def test_create_user(endpoints):
    response = requests.post(endpoints.get("register_user"))
    assert response.status_code == 200
    user_id = response.json().get("user_id")
    assert bool(re.match(r'^user-[a-zA-Z0-9]+$', user_id))

def test_create_user(endpoints):
    response = requests.post(endpoints.get("register_user"))
    user_1 = response.json().get("user_id")
    response = requests.post(endpoints.get("register_user"))
    user_2 = response.json().get("user_id")
    payload = {
        "sender_id": user_1,
        "receiver_id": user_2,
        "sender_id": "Test send message"
    }
    response = requests.post(endpoints.get("send_message"), json=payload)
    assert response.status_code == 200