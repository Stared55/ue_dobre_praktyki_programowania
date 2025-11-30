from typing import Annotated
from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from utils.session import get_db
from schemas.user_schemas import Token
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
from utils.auth import authenticate_user, create_access_token

ACCESS_TOKEN_EXPIRE_MINUTES = 60

router = APIRouter(
    tags=['auth']
)
 
@router.post("/token", include_in_schema=False)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
) -> Token:
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "role": user.role.value}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")
