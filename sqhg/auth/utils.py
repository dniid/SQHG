"""Security utils for SQHG's backend."""

import secrets
from datetime import datetime, timedelta

from jose import JWTError, jwt
from passlib.context import CryptContext

from admin.models import Admin
from core.database import SessionLocal
from core.settings import (
    SECRET_KEY,
    ALGORITHM
)
from user.models import Token

from auth.exceptions import CredentialsException, InvalidToken, ExpiredToken


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


async def get_current_user(token: str):
    database = SessionLocal()
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


async def generate_random_token(token_length: int = 4):
    database = SessionLocal()

    while True:
        token = secrets.token_hex(token_length)

        existing_token = database.query(Token).filter(Token.token == token).first()
        if existing_token is None:
            database.close()
            return token


async def validate_survey_token(token: str):
    database = SessionLocal()

    token = database.query(Token).filter(Token.token == token).first()
    if token is None:
        raise InvalidToken
    if not token.is_active:
        raise ExpiredToken

    return token
