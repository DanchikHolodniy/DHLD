from src.main.api.models.base_model import BaseModel




class Login(BaseModel):
    username: str
    password: str
