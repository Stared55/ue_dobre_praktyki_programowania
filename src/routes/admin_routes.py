from fastapi import APIRouter, Depends, HTTPException, Query, status 
from models.user_models import UserInDB
from schemas.user_schemas import User, UserStatus, CreateUserRequest
from schemas.pagination_schemas import PaginatedResponse 
from utils.auth import get_current_admin_user
from utils import hasher
from utils.pagination import pagination_params
from utils.session import db_dependency
from sqlalchemy.orm import Session
from typing import Tuple

router = APIRouter(
    tags=['Admin'],
    dependencies=[Depends(get_current_admin_user)]
) 

@router.get("/", response_model=PaginatedResponse[User])
def get_users(
    db: db_dependency,
    pagination: Tuple[int, int] = Depends(pagination_params),
):
    skip, limit = pagination

    # total count
    total = db.query(UserInDB).count()

    # fetch users with pagination
    items = db.query(UserInDB).offset(skip).limit(limit).all()

    # convert ORM objects to Pydantic User schema
    users = [
        User(
            id=user.id,
            email=user.email,
            role=user.role.value,         
            status=user.status.value,   
            created_at=user.created_at,
            updated_at=user.updated_at
        )
        for user in items
    ]

    return PaginatedResponse[User](
        total=total,
        skip=skip,
        limit=limit,
        items=users
    )


@router.post("/users/create", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: CreateUserRequest):
    create_user_model = UserInDB(
        email = create_user_request.email,
        password = hasher.get_password_hash(create_user_request.password),
    )
 
    db.add(create_user_model)
    db.commit()

@router.get("/users/{id}",response_model=User)
async def get_user_by_id(db: db_dependency, id: str):
    user = db.query(UserInDB).filter(UserInDB.id == id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user

@router.delete("/users/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_by_id(db: db_dependency, id: str):
    user = db.query(UserInDB).filter(UserInDB.id == id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()

@router.patch("/users/{id}/activate", status_code=status.HTTP_200_OK)
async def activate_user(db: db_dependency, id: str):
    user = db.query(UserInDB).filter(UserInDB.id == id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.status == UserStatus.ACTIVE:
        raise HTTPException(status_code=400, detail="User is already active")

    user.status = UserStatus.ACTIVE
    db.commit()
    return {"msg": "User activated successfully"}

@router.patch("/users/{id}/block", status_code=status.HTTP_200_OK)
async def block_user(db: db_dependency, id: str):
    user = db.query(UserInDB).filter(UserInDB.id == id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.status == UserStatus.BLOCKED:
        raise HTTPException(status_code=400, detail="User is already blocked")

    user.status = UserStatus.BLOCKED
    db.commit()
    return {"msg": "User blocked successfully"}