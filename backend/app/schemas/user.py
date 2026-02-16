from pydantic import BaseModel

class OwnerRegister(BaseModel):
    name: str
    mobile: str
    password: str
    language: str | None = "ta"
    is_milkman: bool = False   # if owner also collects milk

class MilkmanCreate(BaseModel):
    name: str
    mobile: str
    password: str
    language: str | None = "ta"
    
class UserLogin(BaseModel):
    mobile: str
    password: str
