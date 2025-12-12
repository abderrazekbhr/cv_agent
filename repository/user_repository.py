from sqlalchemy.orm import Session
from models.user import User
from schemas.user_schema import UserCreate, UserRead,UserUpdate 

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user(self, email: str)-> UserRead | None:
        user = self.db.query(User).filter(User.email == email).first()
        if user:
            return UserRead(**user.__dict__)
        return None

    def create_user(self, user: UserCreate):
        db_user = User(**user.__dict__)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return UserRead(**db_user.__dict__)

    def get_all_users(self):
        return [UserRead(**user.__dict__) for user in self.db.query(User).all()]
    
    
    
    def delete_user(self, email: str):
        user = self.db.query(User).filter(User.email == email).first()
        if user:
            self.db.query(User).filter(User.email == email).delete()
            self.db.commit()
            return True
        return False
    
    
    def update_user(self, email: str, user_update: UserUpdate):
        user = self.db.query(User).filter(User.email == email).first()
        if user:
            for var, value in vars(user_update).items():
                if value is not None:
                    setattr(user, var, value)
            self.db.commit()
        return user
    
    
    