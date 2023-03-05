from fastapi import APIRouter, Header, Depends, HTTPException,File,UploadFile
from Entity.entity import *
from Service.druidService import DruidService
from Service.userService import UserService
from typing import Optional, List , Union
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from pprint import pprint
from fastapi.responses import StreamingResponse, FileResponse
import random

class DruidQuery(BaseModel):
    start_date: str
    end_date: str
    ticker_table: str

router = APIRouter(prefix="/data", tags=["data"])
druidService = DruidService()
userService = UserService()

@router.post("/data")
async def get_all(DruidQuery: DruidQuery):
	return await druidService.load_ticker_data(DruidQuery.start_date, DruidQuery.end_date, DruidQuery.ticker_table)