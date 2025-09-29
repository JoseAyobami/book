from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from app.schemas.user import Token, TokenData, UserCreate, UserResponse, UserUpdate
from app.models.user import User as UserModel
from app.database import get_db
from fastapi.security import OAuth2PasswordRequestForm
from app.deps import  get_current_user
from app.crud.user import UserCrud
from app.auth import create_access_token, create_refresh_token
from app.deps import security
from jose import JWTError, jwt
from datetime import timedelta
from app.setting import settings
from app.limiter import limiter
from app.logger import get_logger


router = APIRouter(prefix="/users", tags=["User"])

logger = get_logger(__name__)

@router.post("/register", response_model=UserResponse, status_code=201)
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    try:
        logger.info(f"Registering user: {user_data.email}")
        new_user = UserCrud.create_user(db, user_data)
        if not new_user:
            raise HTTPException(status_code=400, detail="User already exists")
        db.commit()
        logger.info(f"User registered: {new_user.email}")
    except Exception as e:
        db.rollback()
        logger.error(f"Error registering user: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    return UserResponse.model_validate(new_user)

@router.post("/create-admin", response_model=UserResponse, status_code=201)
def register_admin(user_data: UserCreate, db: Session = Depends(get_db)):
    try:
        logger.info(f"Registering admin: {user_data.email}")
        new_admin = UserCrud.create_admin(db, user_data)
        if not new_admin:
            raise HTTPException(status_code=400, detail="User already exists")
        db.commit()
        logger.info(f"Admin registered: {new_admin.email}")
    except Exception as e:
        db.rollback()
        logger.error((f"Error registering admin: {e}"))  
        raise HTTPException(status_code=400, detail=str(e))
    return UserResponse.model_validate(new_admin)


@router.post("/login", response_model=Token)
@limiter.limit("5/minutes")
def login_user(request: Request, user_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    logger.info(f"User login attempt: {user_data.username}")
    access_token = UserCrud.login_user(db, user_data.username, user_data.password)
    if not access_token:
        logger.warning(f"Invalid login credentials for user: {user_data.username}")
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    logger.info(f"User logged in successfully: {user_data.username}")
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserResponse)
def get_me(current_user: UserModel=Depends(get_current_user)):
    logger.info(f"Fetching profile for user: {current_user.email}")
    return current_user

@router.put("/me", response_model=UserResponse)
def update_user(update_data: UserUpdate, db: Session = Depends(get_db),current_user: UserModel = Depends(get_current_user)
):
    try:
        logger.info(f"Updating profile for user: {current_user.email}")
        updated_user = UserCrud.update_user(db, current_user.id, update_data)
        if not updated_user:
            raise HTTPException(status_code=404, detail="User not found")
        db.commit()
        logger.info(f"Profile updated for user: {current_user.email}")
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating profile for user {current_user.email}: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    return updated_user


@router.post("/refresh", response_model=Token, status_code=status.HTTP_200_OK)
def refresh_access_token(
    token: str = Depends(security),
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        email: str = payload.get("sub")
        token_type: str = payload.get("token_type")

        if email is None or token_type != "refresh":
            logger.warning(f"Invalid token payload: email={email}, token_type={token_type}")
            raise credentials_exception

        logger.info(f"Token refresh requested for: {email}")
        token_data = TokenData(email=email)

    except JWTError as e:
        logger.error(f"JWT decode failed: {e}", exc_info=True)
        raise credentials_exception

    user = UserCrud.get_user_by_email(db, email=token_data.email)
    if user is None:
        logger.warning(f"User not found during token refresh: {token_data.email}")
        raise credentials_exception

    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    refresh_token_expires = timedelta(days=settings.refresh_token_expire_days)

    access_token = create_access_token(
        data={"sub": user.email, "token_type": "access"},
        expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(
        data={"sub": user.email, "token_type": "refresh"},
        expires_delta=refresh_token_expires
    )

    logger.info(f"New tokens issued for: {user.email}")
    return Token(
        access_token=access_token,
        token_type="bearer",
        refresh_token=refresh_token
    )
    

@router.post("/logout")
def logout(current_user: UserModel=Depends(get_current_user)):
    logger.info(f"User logged out: {current_user.email}")
    return {"msg": f"User {current_user.email} logged out successfully."}


