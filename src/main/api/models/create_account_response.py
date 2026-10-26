from src.main.api.models.base_model import BaseModel




class AccountResponse(BaseModel):
    id: int
    number: int
    balance: float
