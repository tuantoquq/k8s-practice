from fastapi import APIRouter, Header, Depends, HTTPException,File,UploadFile
from Entity.entity import *
from Service.userService import UserService
from typing import Optional, List , Union
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from pprint import pprint
from fastapi.responses import StreamingResponse, FileResponse
import random

class RegUser(BaseModel):
    Name : str
    Username :str
    Password : str

class Login(BaseModel):
    Username: str
    Password: str
    Role: int

router = APIRouter(prefix="/user", tags=["user"])
userService = UserService()

async def get_current_active_user(current_user: User = Depends(userService.get_current_user)):
	if current_user.IsActive == 0:
		raise HTTPException(status_code=400, detail="Inactive user")
	return current_user

@router.post("/register")
async def register(userReg: RegUser):
    id_ = random.randint(100000,1000000)
    while len(await userService.get_user_by_id(Id=id_)) > 0:
        id_ = random.randint(100000,1000000)
    user = User(Id = id_, Role = 1, IsActive = True, **userReg.dict())
    return await userService.register([user])
    
@router.post("/login")
async def login(form_data: Login):
    return await userService.authenticate(form_data)

@router.get("/me", response_model = User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
	return current_user

@router.get("/lock/{Id}")
async def lock(Id:str, current_admin: User = Depends(userService.get_current_user_is_admin)):
    return await userService.lock(Id, 0)

@router.get("/unlock/{Id}")
async def unlock(Id:str, current_admin: User = Depends(userService.get_current_user_is_admin)):
    return await userService.lock(Id, 1)

@router.get("/{Id}")
async def get_by_id(Id:str, current_admin: User = Depends(userService.get_current_user_is_admin)):
    return await userService.get_user_by_id(Id)