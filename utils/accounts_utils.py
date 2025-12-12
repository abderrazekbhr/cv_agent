from requests import Session
from models.user import User
from schemas.user_schema import LoginUser
from repository.user_repository import UserRepository
from config.authentication import verify_password


def check_user_connection(login_data: LoginUser,db: Session):
    repository=UserRepository(db)
    user=repository.db.query(User).filter(User.email==login_data.email).first()
    if not user:
        return False
    if not verify_password(login_data.password,user.password):
        return False
    return True


