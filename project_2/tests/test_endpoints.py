import re
import requests

def test_create_user(endpoints):
    response = requests.post(endpoints.get("register_user"), json={"password": "test-123"})
    assert response.status_code == 200
    user_id = response.json().get("user_id")
    assert bool(re.match(r'^user-[a-zA-Z0-9]+$', user_id))

def test_check_messages(endpoints):
    response = requests.post(endpoints.get("register_user"), json={"password": "test-123"})
    user_id = response.json().get("user_id")
    payload = {
        "user_id": user_id,
        "password": "test-123"
    }
    response = requests.post(endpoints.get("check_messages"), json=payload)
    assert response.status_code == 200
    assert response.json().get("messages") == []

def test_send_message(endpoints):
    response = requests.post(endpoints.get("register_user"), json={"password": "test-123"})
    user_1 = response.json().get("user_id")
    response = requests.post(endpoints.get("register_user"), json={"password": "test-123"})
    user_2 = response.json().get("user_id")
    payload = {
        "sender_id": user_1,
        "password": "test-123",
        "receiver_id": user_2,
        "message": "Test send message"
    }
    response = requests.post(endpoints.get("send_message"), json=payload)
    assert response.status_code == 200
    assert response.json() == {'message': f'Message sent to {user_2}.'}
    response = requests.post(endpoints.get("check_messages"), json={"user_id": user_2, "password": "test-123"})
    assert response.json().get("messages")[-1].get("message") == payload.get("message")

def test_block_user(endpoints):
    response = requests.post(endpoints.get("register_user"), json={"password": "test-123"})
    user_1 = response.json().get("user_id")
    response = requests.post(endpoints.get("register_user"), json={"password": "test-123"})
    user_2 = response.json().get("user_id")
    payload = {
        "user_id": user_1,
        "password": "test-123",
        "block_user_id": user_2
    }
    response = requests.post(endpoints.get("block_user"), json=payload)
    assert response.status_code == 200
    assert response.json() == {'message': f"You have blocked {payload.get('block_user_id')}."}
    payload = {
        "sender_id": user_2,
        "password": "test-123",
        "receiver_id": user_1,
        "message": "Test send message"
    }
    response = requests.post(endpoints.get("send_message"), json=payload)
    assert response.status_code == 403
    assert response.json() == {'message': f"You are unable to send messages to {payload.get('receiver_id')}."}

def test_create_group(endpoints):
    response = requests.post(endpoints.get("register_user"), json={"password": "test-123"})
    user_id = response.json().get("user_id")
    payload = {
        "members": f"{user_id}"
    }
    response = requests.post(endpoints.get("create_group"), json=payload)
    assert response.status_code == 200
    group_id = response.json().get("group_id")
    assert bool(re.match(r'^group-[a-zA-Z0-9]+$', group_id))

def test_add_remove_users(endpoints):
    response = requests.post(endpoints.get("register_user"), json={"password": "test-123"})
    user_id = response.json().get("user_id")
    payload = {
        "members": f"{user_id}"
    }
    response = requests.post(endpoints.get("create_group"), json=payload)
    group_id = response.json().get("group_id")
    response = requests.post(endpoints.get("register_user"), json={"password": "test-123"})
    user_id = response.json().get("user_id")
    payload = {
        "group_id": group_id,
        "user_id": user_id,
        "action": "add"
    }
    response = requests.post(endpoints.get("add_remove_users"), json=payload)
    assert response.status_code == 200
    assert response.json().get("message") == f"{user_id} has been added to the group."

    payload = {
        "group_id": group_id,
        "user_id": user_id,
        "action": "remove"
    }
    response = requests.post(endpoints.get("add_remove_users"), json=payload)
    assert response.status_code == 200
    assert response.json().get("message") == f"{user_id} has been removed from the group."

    response = requests.post(endpoints.get("add_remove_users"), json=payload)
    assert response.status_code == 400
    assert response.json().get("message") == f"Invalid action or user already in desired state."

def test_send_group_message(endpoints):
    response = requests.post(endpoints.get("register_user"), json={"password": "test-123"})
    user_1 = response.json().get("user_id")
    response = requests.post(endpoints.get("register_user"), json={"password": "test-123"})
    user_2 = response.json().get("user_id")
    payload = {
        "members": f"{user_1}, {user_2}"
    }
    response = requests.post(endpoints.get("create_group"), json=payload)
    group_id = response.json().get("group_id")
    group_message = "Hello group!"
    payload = {
        "sender_id": user_1,
        "password": "test-123",
        "group_id": group_id,
        "message": group_message
    }
    response = requests.post(endpoints.get("send_group_message"), json=payload)
    assert response.status_code == 200

    payload = {
        "user_id": user_2,
        "password": "test-123"
    }
    response = requests.post(endpoints.get("check_messages"), json=payload)
    assert response.status_code == 200
    assert response.json().get("messages")[-1].get("message") == group_message