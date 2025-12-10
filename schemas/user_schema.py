from pydantic import BaseModel


class LoginUser(BaseModel):
    email:str
    password:str
    
class UserCreate(BaseModel):
    email: str
    username: str
    name: str
    prename: str
    password: str

class UserRead(BaseModel):
    email: str
    username: str
    name: str
    prename: str

    class Config:
        orm_mode = True
        
        
class UserUpdate(BaseModel):
    username: str | None = None
    name: str | None = None
    prename: str | None = None
    password: str | None = None