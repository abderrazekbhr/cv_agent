from sqlalchemy.orm import Session
from models.user import User
from schemas.user_schema import UserCreate, UserRead,UserUpdate 

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user(self, email: str)-> UserRead | None:
        result = self.db.query(User).filter(User.email == email).first()
        return UserRead(result) if result else None

    def create_user(self, user: UserCreate):
        db_user = User(name=user.name, email=user.email)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user


    def get_all_users(self):
        return [UserRead(user) for user in self.db.query(User).all()]
    
    
    def delete_user(self, email: str):
        user = self.db.query(User).filter(User.email == email).first()
        if user:
            self.db.delete(user)
            self.db.commit()
        return user
    
    
    def update_user(self, email: str, user_update: UserUpdate):
        user = self.db.query(User).filter(User.email == email).first()
        if user:
            for var, value in vars(user_update).items():
                if value is not None:
                    setattr(user, var, value)
            self.db.commit()
        return user