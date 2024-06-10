import pytest
import requests

def pytest_addoption(parser):
    parser.addoption("--url", action="store", help="API base URL")

@pytest.fixture
def endpoints(request):
    url = request.config.getoption("--url")
    endpoints = {
        "register_user": f"{url}/register_user",
        "block_user": f"{url}/block_user",
        "create_group": f"{url}/create_group",
        "add_remove_users": f"{url}/add_remove_users",
        "send_group_message": f"{url}/send_group_message",
        "send_message": f"{url}/send_message",
        "check_messages": f"{url}/check_messages"
    }
    return endpoints