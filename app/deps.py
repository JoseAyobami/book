from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
import jwt
from jwt.exceptions import InvalidTokenError
from app.database import get_db
from app.models.base import UserRole    
from app.setting import settings
from app.models.user import User as UserModel
from fastapi.security import HTTPBearer


security = HTTPBearer()



def get_current_user(token: str = Depends(security), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token.credentials, settings.secret_key, algorithms=[settings.algorithm])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    user = db.query(UserModel).filter(UserModel.email == email).first()
    if user is None:
        raise credentials_exception
    return user



def get_current_admin(current_user: UserModel = Depends(get_current_user)):
    if current_user.role != UserRole.admin.value:  
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user

# def get_current_admin(user: UserModel = Depends(get_current_user)):
#     if user.role != UserRole.admin:
#         raise HTTPException(status_code=403, detail="Admin access required")
#     return user