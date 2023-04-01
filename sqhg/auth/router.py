"""Auth's FastAPI router endpoints for SQHG's backend."""

from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from admin.models import Admin
from admin.schemas import AdminSchema
from core.database import Database
from core.settings import (
    ACCESS_TOKEN_EXPIRE_MINUTES
)

from auth.schemas import (
    JWToken
)
from auth.utils import (
    authenticate_user,
    create_access_token,
    get_current_user
)
from auth.exceptions import (
    InvalidCredentials
)


router = APIRouter()


@router.post("/token", response_model=JWToken)
async def login_for_access_token(request: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 database: Session = Depends(Database)):
    form_user = database.query(Admin).filter(Admin.email == request.email).first()
    user = authenticate_user(form_user, request.password)
    if not user:
        raise InvalidCredentials
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=AdminSchema)
async def read_users_me(
    current_user: Annotated[Admin, Depends(get_current_user)]
):
    return current_user
