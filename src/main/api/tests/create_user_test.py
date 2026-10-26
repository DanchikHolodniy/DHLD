import pytest

from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.create_user import CreateUserRequest
from src.main.api.db.crud.user_crud import UserCrudDb as UserCrud




@pytest.mark.api
class TestCreateUser:
    @pytest.mark.parametrize(
        "create_user_request",
        [RandomModelGenerator.generate(CreateUserRequest)],
    )
    def test_create_user_valid(self, db_session: Session, api_manager: ApiManager, create_user_request: CreateUserRequest):
        response = api_manager.admin_steps.create_user(create_user_request)
        assert create_user_request.username == response.username, "Логин в ответе сервера не совпадает с отправленным"
        assert create_user_request.role == response.role, "Роль в ответе сервера не совпадает с отправленной"

        user_from_db = UserCrud.get_user_by_username(db_session, create_user_request.username)
        assert user_from_db is not None, "Пользователь не найден в DB"
        assert user_from_db.username == create_user_request.username, "Логин пользователя не совпадает с DB"


    @pytest.mark.parametrize(
        "username, password",
        [
            ("абв", "Pas!sw0rd"),
            ("ab", "Pas!sw0rd"),
            ("abv!", "Pas!sw0rd"),
            ("max1", "Pas!sw0rд"),
            ("max2", "Pas!sw0"),
            ("max3", "pas!sw0rd"),
            ("max4", "PAS!SW0RD"),
            ("max5", "PASSSW0RD"),
            ("max6", "PAS!SWRRD"),
        ]
    )
    def test_create_user_invalid(self, db_session: Session, api_manager: ApiManager, username: str, password: str):
        create_user_request = CreateUserRequest(username=username, password=password, role="ROLE_USER")
        api_manager.admin_steps.create_user_invalid(create_user_request)

        user_from_db = UserCrud.get_user_by_username(db_session, username)
        assert user_from_db is None, "Пользователь был создан, ошибка"
