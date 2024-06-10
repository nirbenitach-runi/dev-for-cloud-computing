import re
import requests

def test_create_user(endpoints):
    response = requests.post(endpoints.get("register_user"))
    assert response.status_code == 200
    user_id = response.json().get("user_id")
    assert bool(re.match(r'^user-[a-zA-Z0-9]+$', user_id))

def test_check_messages(endpoints):
    response = requests.post(endpoints.get("register_user"))
    user_id = response.json().get("user_id")
    payload = {
        "user_id": user_id
    }
    response = requests.post(endpoints.get("check_messages"), json=payload)
    assert response.status_code == 200
    assert response.json().get("messages") == []

def test_send_message(endpoints):
    response = requests.post(endpoints.get("register_user"))
    user_1 = response.json().get("user_id")
    response = requests.post(endpoints.get("register_user"))
    user_2 = response.json().get("user_id")
    payload = {
        "sender_id": user_1,
        "receiver_id": user_2,
        "message": "Test send message"
    }
    response = requests.post(endpoints.get("send_message"), json=payload)
    assert response.status_code == 200
    assert response.json() == {'message': f'Message sent to {user_2}.'}
    response = requests.post(endpoints.get("check_messages"), json={"user_id": user_2})
    assert response.json().get("messages")[-1].get("message") == payload.get("message")

def test_block_user(endpoints):
    response = requests.post(endpoints.get("register_user"))
    user_1 = response.json().get("user_id")
    response = requests.post(endpoints.get("register_user"))
    user_2 = response.json().get("user_id")
    payload = {
        "user_id": user_1,
        "block_user_id": user_2
    }
    response = requests.post(endpoints.get("block_user"), json=payload)
    assert response.status_code == 200
    assert response.json() == {'message': f"You have blocked {payload.get('block_user_id')}."}
    payload = {
        "sender_id": user_1,
        "receiver_id": user_2,
        "message": "Test send message"
    }
    response = requests.post(endpoints.get("send_message"), json=payload)
    assert response.status_code == 403
    assert response.json() == {'message': f"You are unable to send messages to {payload.get('receiver_id')}."}

def test_create_group(endpoints):
    ...

def add_remove_users(endpoints):
    ...