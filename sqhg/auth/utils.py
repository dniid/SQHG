"""Security utils for SQHG's backend."""

from datetime import datetime, timedelta

from fastapi import Depends
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from admin.models import Admin
from core.database import Database
from core.settings import (
    SECRET_KEY,
    ALGORITHM
)

from auth.exceptions import CredentialsException


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(user: Admin, password: str):
    if not verify_password(password, user.password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta if expires_delta else datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({'exp': expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: str, database: Session):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get('sub')
        if email is None:
            raise CredentialsException
    except JWTError as error:
        raise CredentialsException from error
    user = database.query(Admin).filter(Admin.email == email).first()
    database.close()
    if user is None:
        raise CredentialsException
    return user
