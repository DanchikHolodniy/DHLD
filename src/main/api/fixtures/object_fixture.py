import pytest, logging

from typing import List, Any
from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_user_response import CreateResponse




@pytest.fixture
def create_object():
    object: List[Any] = []
    yield object
    clean_user(object)


def clean_user(object: List[Any]):
    api_manager = ApiManager(object)
    for u in object:
        if isinstance(u, CreateResponse):
            api_manager.admin_steps.delete_user(u.id)
        else:
            logging.warning(f"Error delete user {u.id}")
