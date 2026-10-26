import requests

from src.main.api.configs.config import Config
from src.main.api.models.login_user import Login
from src.main.api.models.login_user_response import LoginUserResponse
from src.main.api.specs.response_spc import ResponseSpc




class Request:
    @staticmethod
    def base_headers():
        return {"Content-Type": "application/json", "accept": "application/json"}


    @staticmethod
    def auth_headers(username: str, password: str):
        request = Login(username=username, password=password)
        response = requests.post(
            url=f"{Config.fetch("backendURL")}/auth/token/login",
            json=request.model_dump(),
            headers=Request.base_headers(),
        )

        if ResponseSpc.response_ok():
            login_user_response = LoginUserResponse(**response.json())
            token = login_user_response.token
            headers = Request.base_headers()
            headers.update({"Authorization": f"Bearer {token}"})
            return headers
        raise Exception("failed to login user")


    @staticmethod
    def unauth_headers():
        return Request.base_headers()
