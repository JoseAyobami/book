from app.schemas.user import UserCreate, UserLogin, UserUpdate
from app.models.user import User as UserModel, UserRole  
from sqlalchemy.orm import Session 
from datetime import timedelta
from sqlalchemy.orm import Session
from app.auth import authenticate_user, create_access_token, hash_password
from app.logger import get_logger

logger = get_logger(__name__)

class UserCrud:
    @staticmethod
    def create_user(db: Session, user_data: UserCreate):
        existing_email = db.query(UserModel).filter(UserModel.email == user_data.email).first()
        if existing_email:
            logger.warning(f"Attempt to register with existing email: {user_data.email}")
            return None        

        hashed_password = hash_password(user_data.password)
        new_user = UserModel(
            name=user_data.name,
            email=user_data.email,
            password_hash=hashed_password,  
            role=UserRole.user.value
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    
    @staticmethod
    def create_admin(db: Session, user_data: UserCreate):
        existing_email = db.query(UserModel).filter(UserModel.email == user_data.email).first()
        if existing_email:
            logger.warning(f"Attempt to register with existing email: {user_data.email}")
            return None        

        hashed_password = hash_password(user_data.password)
        new_admin = UserModel(
            name=user_data.name,
            email=user_data.email,
            password_hash=hashed_password,
            role=UserRole.admin.value  
        )
        db.add(new_admin)
        db.commit()
        db.refresh(new_admin)
        return new_admin
    
    @staticmethod
    def login_user(db: Session, user: UserLogin):
        db_user = authenticate_user(db, user.email, user.password)
        if not db_user:
            logger.warning(f"Invalid login credentials for user: {user.email}")
            return None
        access_token_expires = timedelta(minutes=30)
        access_token = create_access_token(
            data={"sub": db_user.email, "role": db_user.role}, expires_delta=access_token_expires
        )
        return access_token

    

    @staticmethod
    def update_user(db: Session, user_id: str, update_data: UserUpdate):
        user = db.query(UserModel).filter(UserModel.id == user_id).first()
        if not user:
            return None

        # Update fields if provided
        if update_data.name is not None:
            user.name = update_data.name

        if update_data.password is not None:
            user.password_hash = hash_password(update_data.password)

        db.commit()
        db.refresh(user)
        return user
    
    @staticmethod
    def get_user_by_email(db: Session, email: str):
        return db.query(UserModel).filter(UserModel.email == email).first()

        
    @staticmethod
    def delete_user(db: Session, user: UserModel):
        db.delete(user)
        db.flush()
        return {"detail": "User deleted"}


user_crud = UserCrud()    
    
    
    

    
