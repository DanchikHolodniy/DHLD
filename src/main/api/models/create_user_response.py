from src.main.api.models.base_model import BaseModel


class CreateResponse(BaseModel):
    id: int
    role: str
    username: str
    password: str
