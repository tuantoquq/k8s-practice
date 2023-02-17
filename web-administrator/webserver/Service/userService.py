from Repository.userRepository import UserRepository
from Entity.entity import *
from fastapi.security import OAuth2PasswordBearer
from fastapi import  Depends
from .utils import JWTUtils
from fastapi import HTTPException
from datetime import timedelta
from config import Settings
from typing import Optional, List
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.security import HTTPBearer
import pandas as pd
import io, time
import pprint

reusable_oauth2 = HTTPBearer(
        scheme_name='Authorization'
    )
class UserService:
    def __init__(self, ):
        self.connector = UserRepository()
        self.settings = Settings()

    async def lock(self, Id: int, status: int):
        return await self.connector.lock(Id, status)

    async def register(self, users: List[User]):
        processed = []
        for user in users:
            user.Password = JWTUtils.get_password_hash(user.Password)
            processed.append(user)
        return await self.connector.insert(processed)
    
    async def change_password(self,old_password, new_password, current_user: User):
        if JWTUtils.verify_password(old_password, current_user.password):
            hashed_password = JWTUtils.get_password_hash(new_password)
            res = await self.connector.update_password(current_user.Id, hashed_password)
            return res
        else:
            raise HTTPException(status_code=402, detail="Wrong old password")

    async def get_user_by_id(self, Id:int):
        return await self.connector.get_user_by_id(Id)

    async def get_user_by_user_name(self, userName: str):
        return await self.connector.get_user_by_user_name(userName)

    async def authenticate(self, login_object):
        user = await self.get_user_by_user_name(login_object.Username)

        if (len(user)) == 0:
            raise HTTPException(status_code=402, detail = "Wrong username")
        if user[0].Role != login_object.Role:
            raise HTTPException(status_code=402, detail = "Wrong role")
        if user[0].IsActive == 0:
            return "No permission!"
        
        user = user[0]
        if JWTUtils.verify_password(login_object.Password, user.Password):
            session_time = timedelta(minutes=self.settings.expire_minutes)
            return JWTUtils.create_access_token(data={"username":login_object.Username}, expires_delta = session_time)
        else:
            raise HTTPException(status_code = 402, detail = "Wrong password!")

    async def get_current_user(self, token: str = Depends(reusable_oauth2)):
        userName = JWTUtils.get_current_username(token)
        user = await self.get_user_by_user_name(userName)
        if len(user):
            return user[0]
        else:
            raise HTTPException(status_code=402, detail="Unautorized")

    async def get_current_user_is_admin(self, token: str = Depends(reusable_oauth2)):
        userName = JWTUtils.get_current_username(token)
        users = await self.get_user_by_user_name(userName)
        if len(users) and users[0].Role == 0:
            return users[0]
        else:
            raise HTTPException(status_code=402, detail="Unautorized")