from fastapi import APIRouter, Body, HTTPException
from pydantic import BaseModel

router=APIRouter()

class UserCreateRequest(BaseModel):
    name:str
    prename:str
    username: str
    email: str
    password: str
        




@router.post("/")
def create_account(creation_data: UserCreateRequest):
    pass

@router.delete("/")
def delete_account(email: str):
    pass

@router.patch("/{email}")
def update_account(email: str, update_data: UserCreateRequest):
    pass


@router.post("/login")
def login():
    pass