import mock
import pytest

from api.presentation.mappings import UserLoginRequestMapping
from api.application.use_cases import UserUseCase, LoginNotAuthorized


@mock.patch.object(UserUseCase, "login")
def test_user_login(login_mock, user_login_mapping, app):
    
    login_mock.return_value = "token_abc"
    payload = {"username": "test", "password": "test"}
    response = app.post(
        "/api/v1/user/login",
        json=payload
    )
    
    assert response.json == {'token': 'token_abc'}
    assert response.status_code == 200


@mock.patch.object(UserUseCase, "login")
def test_user_login_failure(login_mock, user_login_mapping, app):
    
    login_mock.side_effect = LoginNotAuthorized("Invalid credentials")
    payload = {"username": "test", "password": "test"}
    response = app.post(
        "/api/v1/user/login",
        json=payload
    )
    assert response.json == {'message': 'Invalid credentials'}
    assert response.status_code == 401