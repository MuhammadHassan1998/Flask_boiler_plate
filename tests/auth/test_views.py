from tests.config_test import *
from flask import session


def test_add_user(client):
    response = client.post("/api/auth/register", data={
        "email": "muhammad@devsinc.com",
        "password": "12345",
    })
    assert response.status_code == 302


def test_access_session(client):
    with client:
        client.post(
            "/api/auth/login", data={"email": "muhammad@devsinc.com", "password": "12345"})
        assert session["email"] == "muhammad@devsinc.com"
