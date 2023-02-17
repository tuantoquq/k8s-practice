from fastapi import APIRouter, Header, Depends, HTTPException,File,UploadFile
from Entity.entity import *
from Service.auditService import AuditService
from Service.userService import UserService
from typing import Optional, List , Union
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from pprint import pprint
from fastapi.responses import StreamingResponse, FileResponse
import random

router = APIRouter(prefix="/audit", tags=["audit"])
auditService = AuditService()
userService = UserService()

@router.get("/getall", response_model = List[AuditResponse])
async def get_all(current_admin: User = Depends(userService.get_current_user_is_admin)):
    return await auditService.get_all()