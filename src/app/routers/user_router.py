from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, Security
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, SecurityScopes
from ..schema.base import CommRes
from ..schema.user import  UserSchema
from ..services.user_service import UserService
from ..utils.auth_util import oauth2_scheme

user_router =  APIRouter(prefix="/user", tags=["User module"], responses={
    404: {"description": "Notfound"}
})


async def get_current_user(security_scopes: SecurityScopes, token: Annotated[str, Depends(oauth2_scheme)],service: UserService = Depends()):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )
    user,token_data=await service.get_current_user(authenticate_value, token)
    return user
async def get_current_active_user(
    current_user: UserSchema = Security(get_current_user, scopes=[]),
):
    return current_user
@user_router.post("/register", response_model=CommRes)
def create(user: UserSchema, service: UserService = Depends()):
    return CommRes.success(service.create(user))

@user_router.get("/all", response_model=CommRes)
def get_all_users(current_user: UserSchema = Security(get_current_active_user), service: UserService = Depends()):
    return CommRes.success(service.get_list(None))

@user_router.get("/id/{user_id}", response_model=CommRes, status_code=status.HTTP_200_OK)
def get_user(user_id: str, service: UserService = Depends()):
   return CommRes.success(service.get(user_id))

@user_router.put("/", response_model=CommRes, status_code=status.HTTP_200_OK)
def update_user(user_update: UserSchema, service: UserService = Depends()):
    return CommRes.success(service.update(user_update))

@user_router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: str,service: UserService = Depends()):
    service.delete(user_id)
    return

@user_router.post("/token", status_code=status.HTTP_200_OK)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),service: UserService = Depends()):
    return service.login(form_data.username, form_data.password)


@user_router.get("/me", response_model=CommRes, status_code=status.HTTP_200_OK)
def read_users_me(current_user=Depends(get_current_active_user)):
    return CommRes.success(current_user)
@user_router.get("/how-to-use-authentication-exampe", response_model=CommRes, status_code=status.HTTP_200_OK)
def read_users_me(current_user: UserSchema = Security(get_current_active_user)):
    return CommRes.success(current_user)

