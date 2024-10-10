import mock
import pytest

from flask import current_app
from api.domain.models.user import User


def test_authenticate_success(app):
    current_app.config["LOGIN_USERNAME"] = "username"
    current_app.config["LOGIN_PASSWORD"] = "senha321"
    
    username = User.authenticate(
        username="username",
        password="senha321"
    )
    
    assert username == "username"


def test_authenticate_failure(app):
    current_app.config["LOGIN_USERNAME"] = "username"
    current_app.config["LOGIN_PASSWORD"] = "senha321"
    
    username = User.authenticate(
        username="wrong_username",
        password="senha321"
    )
    
    assert username is None