from fastapi import APIRouter, Body, Depends, HTTPException
from pydantic import BaseModel
from requests import Session
from config.db import get_db
from repository.user_repository import UserRepository
from schemas.user_schema import UserCreate, UserRead, UserUpdate

router=APIRouter()


@router.post("/")
def create_account(creation_data: UserCreate, db: Session=Depends(get_db)):
    pass

@router.delete("/")
def delete_account(email: str,db: Session=Depends(get_db)):
    pass

@router.patch("/{email}")
def update_account(email: str, update_data: UserUpdate,db: Session=Depends(get_db)):
    pass


@router.post("/login")
def login():
    pass