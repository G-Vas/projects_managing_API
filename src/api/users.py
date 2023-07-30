from datetime import timedelta
from typing_extensions import Annotated
from fastapi import APIRouter
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from services.auth import AuthService, oauth2_scheme
from core.conf import ACCESS_TOKEN_EXPIRE_MINUTES
from schemas.users import UserSchema, UserInDBSchema
from schemas.token import TokenSchema
from repositories.users import UserRepository
from sqlalchemy.ext.asyncio import AsyncSession
from db.conf_db import get_db
from models.models import User

router = APIRouter()


@router.post("/token", response_model=TokenSchema)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 db: Annotated[AsyncSession, Depends(get_db)]) -> dict:

    repo = UserRepository(db)
    service = AuthService(repo=repo)
    user = await service.authenticate_user(email=form_data.username, password=form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = service.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me", response_model=UserSchema)
async def read_users_me(db: Annotated[AsyncSession, Depends(get_db)],
                        token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    repo = UserRepository(db=db)
    current_user = await AuthService(repo=repo).get_current_user(token=token)
    return current_user


@router.post("/add", response_model=UserSchema)
async def add(user: UserInDBSchema,
              db: Annotated[AsyncSession, Depends(get_db)]) -> User:
    repo = UserRepository(db=db)
    service = AuthService(repo=repo)
    response = await service.add_user(user)
    return response
