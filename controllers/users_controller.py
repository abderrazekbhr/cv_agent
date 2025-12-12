from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.params import Query
from pydantic import BaseModel
from requests import Session
from config.db import get_db
from repository.user_repository import UserRepository
from schemas.user_schema import UserCreate, UserRead, UserUpdate,LoginUser
from config.authentication import get_password_hash
from utils.accounts_utils import check_user_connection

router=APIRouter()


@router.post("/signup", response_model=UserRead)
def create_account(creation_data: UserCreate, db: Session=Depends(get_db)):
    repository=UserRepository(db)
    creation_data.password=get_password_hash(creation_data.password)
    creation_data_exist=repository.get_user(creation_data.email)
    if creation_data_exist:
        raise HTTPException(status_code=400, detail="User already exists")
    return repository.create_user(creation_data)


@router.post("/login",response_model=dict)
def login(login_data: LoginUser = Body(...), db: Session=Depends(get_db)):
    correct_connection=check_user_connection(login_data, db)
    if not correct_connection:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return {"detail": "Login successful"}


@router.delete("/")
def delete_account(email: str=Query(...),db: Session=Depends(get_db)):
    repository=UserRepository(db)
    result=repository.delete_user(email)
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    return {"detail": "User deleted successfully"}


@router.patch("/")
def update_account(update_data: UserUpdate,email: str=Query(...),db: Session=Depends(get_db)):
    repository=UserRepository(db)
    user=repository.get_user(email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if update_data.password:
        update_data.password=get_password_hash(update_data.password)
    return repository.update(email, update_data)


@router.get("/", response_model=UserRead)
def get_account(email: str=Query(...), db: Session=Depends(get_db)):
    repository=UserRepository(db)
    user=repository.get_user(email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/", response_model=list[UserRead])
def get_all_accounts(db: Session=Depends(get_db)):
    repository=UserRepository(db)
    return repository.get_all_users()
