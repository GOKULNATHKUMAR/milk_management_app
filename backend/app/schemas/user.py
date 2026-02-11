from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    mobile: str
    password: str
    role: str # owner / milkman / owner_milkman
    language: str | None = "ta"
    owner_id: int | None = None

class UserLogin(BaseModel):
    mobile: str
    password: str
