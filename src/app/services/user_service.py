from typing import Annotated, Tuple

import jwt
from fastapi import Depends, HTTPException
from starlette import status

from app.dao.user_dao import UserDao
from app.models.user import User

from app.schema.auth import Token, TokenData
from app.schema.user import UserSchema
from app.services.base import BaseService
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone

from app.utils.auth_util import verify_password, ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, SECRET_KEY, \
    ALGORITHM, get_password_hash, oauth2_scheme


class UserService(BaseService):
    def __init__(self, dao: UserDao = Depends()):

        self.schema = UserSchema
        self.model = User
        self.dao: UserDao = dao

        super().__init__()



    def create(self, user: UserSchema)->UserSchema:
        # 1. Check if user already exists by email
        existing_user = self.dao.get_user_by_email(user.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists."
            )
        # 2. Hash the password
        hashed_password = get_password_hash(user.password)
        # 3. Create the user in the database
        db_user = User(name=user.name, email=user.email, password=hashed_password, remark=user.remark)
        is_created = self.dao.create(db_user)
        user.password = None
        return user
    def update(self, user: UserSchema)->UserSchema:
        user.password=get_password_hash(user.password)
        return super().update(user)
    def get(self, id: str) -> UserSchema:
        res:UserSchema=super().get(id)
        res.password=None
        return res

    def login(self,email:str,password:str):
        user = self.dao.get_user_by_email(email)  # user name is the user email
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        if not verify_password(password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.email},  # "sub" typically references unique user info
            expires_delta=access_token_expires
        )
        return Token(access_token=access_token, token_type="bearer")
    def get_user_by_email(self, email:str) -> UserSchema:
        user = self.dao.get_user_by_email(email)
        return self.model2schema(user, self.schema)

    async def get_current_user(self,authenticate_value,token)->Tuple[UserSchema,TokenData]:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": authenticate_value},
        )
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            email: str = payload.get("sub")
            if email is None:
                raise credentials_exception
            token_scopes = payload.get("scopes", [])
            token_data = TokenData(email=email,scopes=token_scopes)
        except Exception as e:
            raise credentials_exception
        user = self.dao.get_user_by_email(email)
        user.password = None
        if user is None:
            raise credentials_exception

        return self.model2schema(user,UserSchema),token_data
    def get_user_by_token(self,token: str ):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            email: str = payload.get("sub")
            if email is None:
                raise credentials_exception
            token_data = TokenData(email=email)
        except Exception as e:
            raise credentials_exception

        user = self.dao.get_user_by_email(token_data.username)
        if user is None:
            raise credentials_exception
        return user
