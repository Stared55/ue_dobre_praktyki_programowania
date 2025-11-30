from typing import Annotated
from fastapi import Depends, HTTPException, status
from models.user_models import UserInDB, UserStatus, UserRole
from schemas.user_schemas import TokenData
from sqlalchemy.orm import Session
import jwt
from utils import hasher
from utils.session import get_db
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer
from enum import Enum

SECRET_KEY = "2b5d09de4f1a61b759d634a3d1762f85bdadd112e5666f5fddaef27ead2c64c5"
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_user(email: str, db: Session = Depends(get_db)):
    return db.query(UserInDB).filter(UserInDB.email == email).first()


def authenticate_user(email: str, password: str, db: Session = Depends(get_db)):
    print(f"Authenticating user with email: {email}")
    print(f"Authenticating password: {password}")
    user = get_user(email, db)
    print(f"Authenticating user: {user}")
    if not user:
        return False
    if not hasher.verify_password(password, user.password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()

    # Convert Enum values to strings
    for k, v in to_encode.items():
        if isinstance(v, Enum):
            to_encode[k] = v.value

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    # Convert datetime to timestamp
    to_encode.update({"exp": int(expire.timestamp())})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)],db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)

    except jwt.InvalidTokenError:
        raise credentials_exception
    
    user = get_user(email=token_data.email, db=db)

    if not user:
        raise credentials_exception
    
    return user


async def get_current_active_user(
    current_user: Annotated[UserInDB, Depends(get_current_user)],
):
    if current_user.status != UserStatus.ACTIVE:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def get_current_admin_user(
    current_user: Annotated[UserInDB, Depends(get_current_user)]
):
    if not current_user.role == UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this resource",
        )
    if current_user.status != UserStatus.ACTIVE:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this resource",
        )
    return current_user