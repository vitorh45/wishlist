import pytest
import mock

from api.domain.models.user import User
from api.application.use_cases import (
    UserUseCase,
    LoginNotAuthorized
)

@mock.patch.object(User, "authenticate")
@mock.patch.object(User, "generate_access_token")
def test_login_success(generate_access_token_mock, authenticate_mock, user_login_mapping, app):
    authenticate_mock.return_value = user_login_mapping.username
    generate_access_token_mock.return_value = "token_abc"
    token = UserUseCase.login(
        data=user_login_mapping
    )
    
    assert token == "token_abc"
    authenticate_mock.assert_called_once_with(username=user_login_mapping.username, password=user_login_mapping.password)
    generate_access_token_mock.assert_called_once_with(username=user_login_mapping.username)


@mock.patch.object(User, "authenticate")
def test_login_not_authorized(authenticate_mock, user_login_mapping, app):
    authenticate_mock.return_value = None
    
    with pytest.raises(LoginNotAuthorized):
        UserUseCase.login(
        data=user_login_mapping
    )
    authenticate_mock.assert_called_once_with(username=user_login_mapping.username, password=user_login_mapping.password)
