from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
import jwt
from jwt.exceptions import InvalidTokenError
from app.database import get_db
from app.models.base import UserRole    
from app.setting import settings
from app.models.user import User as UserModel
from fastapi.security import OAuth2PasswordBearer



security = OAuth2PasswordBearer(tokenUrl="/users/login")



def get_current_user(token: str = Depends(security), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        email: str = payload.get("sub")
        role: str = payload.get("role")
        if email is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    user = db.query(UserModel).filter(UserModel.email == email).first()
    if user is None:
        raise credentials_exception
    return user


def get_current_admin(current_user: UserModel = Depends(get_current_user), token: str = Depends(security)):
    payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
    role: str = payload.get("role")

    if role != UserRole.admin.value:
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user

