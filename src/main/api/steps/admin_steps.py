from src.main.api.foundation.endpoint import Endpoint
from src.main.api.foundation.requesters.crud_requester import CrudRequester
from src.main.api.foundation.requesters.validate_crud_requester import ValidateCrudRequester
from src.main.api.models.create_user import CreateUserRequest
from src.main.api.models.create_user_credit import CreateUserCreditRequest
from src.main.api.models.login_user import Login
from src.main.api.specs.request_spc import Request
from src.main.api.specs.response_spc import ResponseSpc
from src.main.api.steps.base_steps import BaseSteps




class AdminSteps(BaseSteps):
    def create_user(self, create_user_request: CreateUserRequest):
        response = ValidateCrudRequester(
            Request.auth_headers(username="admin", password="123456"),
            Endpoint.ADMIN_CREATE_USER,
            ResponseSpc.response_ok(),
        ).post(create_user_request)
        self.create_object.append(response)
        return response


    def create_user_invalid(self, create_user_request: CreateUserRequest):
        CrudRequester(
            Request.auth_headers(username="admin", password="123456"),
            Endpoint.ADMIN_CREATE_USER,
            ResponseSpc.response_bad(),
        ).post(create_user_request)


    def create_user_credit(self, create_user_request: CreateUserCreditRequest):
        response = ValidateCrudRequester(
            Request.auth_headers(username="admin", password="123456"),
            Endpoint.ADMIN_CREATE_USER,
            ResponseSpc.response_ok(),
        ).post(create_user_request)
        self.create_object.append(response)
        return response


    def delete_user(self, user_id: int):
        CrudRequester(
            Request.auth_headers(username="admin", password="123456"),
            Endpoint.ADMIN_DELETE_USER,
            ResponseSpc.response_ok(),
        ).delete(user_id)


    def login_user(self, login_user_request: Login):
        response = ValidateCrudRequester(
            Request.unauth_headers(), Endpoint.LOGIN_USER, ResponseSpc.response_ok()
        ).post(login_user_request)
        return response
