from config.db import Base 
from sqlalchemy import Column, Integer, String


class User(Base):
    __tablename__ = "users"
    
    email = Column(String, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    name = Column(String, index=True)
    prename = Column(String, index=True)
    password= Column(String)
    

