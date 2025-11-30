from typing import Annotated
from fastapi import APIRouter, Depends
from models.user_models import UserInDB
from schemas.user_schemas import User
from utils.auth import get_current_active_user
from utils.session import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/users",
    tags=['Users'],
    dependencies=[Depends(get_current_active_user)]
)
@router.get("/me", response_model=User)
async def read_user_me( 
    current_user: Annotated[UserInDB, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
):
    return current_user