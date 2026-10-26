import pytest

from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_user import CreateUserRequest
from src.main.api.models.login_user import Login




@pytest.mark.api
class TestUserLogin:
    def test_admin_login(self, api_manager: ApiManager):
        login_user_request = Login(username="admin", password="123456")
        response = api_manager.admin_steps.login_user(login_user_request)

        assert login_user_request.username == response.user.username
        assert response.user.role == "ROLE_ADMIN"


    def test_user_login(self, api_manager: ApiManager, create_user_request: CreateUserRequest):
        response = api_manager.admin_steps.login_user(create_user_request)

        assert create_user_request.username == response.user.username
        assert response.user.role == "ROLE_USER"
