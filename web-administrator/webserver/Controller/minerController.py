from fastapi import APIRouter, Header, Depends, HTTPException,File,UploadFile
from Entity.entity import *
from Service.minerService import MinerService
from Service.userService import UserService
from Service.auditService import AuditService
from typing import Optional, List , Union
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from pprint import pprint
from fastapi.responses import StreamingResponse, FileResponse
import random
import datetime

router = APIRouter(prefix="/miner", tags=["miner"])
userService = UserService()
minerService = MinerService()
auditService = AuditService()

class NewMiner(BaseModel):
    Name: str
    InputTables: str
    RecursiveRange: int
    GetInputs: str
    Formula: str

class Indicator(BaseModel):
    Day: str
    Value: float

class RawData(BaseModel):
    Day: str
    Height: float
    Low: float
    Open: float
    Close: float
    Volumn: float

class UpdateMiner(BaseModel):
    CreateAt: str
    Formula: str
    GetInputs: str
    Id: int
    InputTables: str
    IsActive: str
    IsSuccess: bool
    Name: str
    RecursiveRange: int
    Schedule: str
    UpdateAt: str

@router.get("/getrawdata", response_model = List[RawData])
async def get_raw_data(_: User = Depends(userService.get_current_user)):
    return None

@router.get("/getindicator", response_model = List[Indicator])
async def get_indicator(_: User = Depends(userService.get_current_user)):
    return None

@router.get("/getlisttable", response_model = List[str])
async def get_list_table(_: User = Depends(userService.get_current_user)):
    return None

@router.get("/getall", response_model = List[MinerResponse])
async def get_all(_: User = Depends(userService.get_current_user_is_admin)):
    return await minerService.get_all()

@router.get("/getownminer", response_model = List[Miner])
async def get_all_own_miner(current_user: User = Depends(userService.get_current_user)):
    return await minerService.get_by_user_id(current_user.Id)

@router.post("/create")
async def create(newMiner: NewMiner, current_user: User = Depends(userService.get_current_user)):
    addMiner = Miner(
        DefineUserId = current_user.Id,
        UserCanUse = '',
        CreateAt = datetime.datetime.now().strftime('%Y/%m/%d/'),
        UpdateAt = datetime.datetime.now().strftime('%Y/%m/%d/'),
        Name = newMiner.Name,
        Schedule = '0 0 * * *',
        InputTables = newMiner.InputTables,
        RecursiveRange = newMiner.RecursiveRange,
        GetInputs = newMiner.GetInputs,
        Formula = newMiner.Formula,
        IsActive = True,
        IsSuccess = True,
        Id = 0
    )
    addedMiner = await minerService.add([addMiner])
    addAudit = Audit(
        Id = 0,
        UserId = current_user.Id,
        ActionId = 0,
        ActionAt = datetime.datetime.now().strftime('%Y/%m/%d/'),
        MinerId = int(addedMiner[0][0])
    )
    await auditService.add([addAudit])
    return addedMiner

@router.post("/update")
async def update(updateMiner: UpdateMiner, current_user: User = Depends(userService.get_current_user)):
    _updateMiner = Miner(
        DefineUserId = current_user.Id,
        UserCanUse = '',
        CreateAt = updateMiner.CreateAt,
        UpdateAt = datetime.datetime.now().strftime('%Y/%m/%d/'),
        Name = updateMiner.Name,
        Schedule = '0 0 * * *',
        IsActive = True,
        Id = updateMiner.Id,
        InputTables = updateMiner.InputTables,
        RecursiveRange = updateMiner.RecursiveRange,
        GetInputs = updateMiner.GetInputs,
        Formula = updateMiner.Formula,
        IsSuccess = updateMiner.IsSuccess
    )
    await minerService.update([_updateMiner])
    addAudit = Audit(
        Id = 0,
        UserId = current_user.Id,
        ActionId = 1,
        ActionAt = datetime.datetime.now().strftime('%Y/%m/%d/'),
        MinerId = updateMiner.Id
    )
    await auditService.add([addAudit])
    return True

@router.post("/delete")
async def delete(deleteMiner: UpdateMiner, current_user: User = Depends(userService.get_current_user)):
    _deleteMiner = Miner(
        DefineUserId = current_user.Id,
        UserCanUse = '',
        CreateAt = deleteMiner.CreateAt,
        UpdateAt = deleteMiner.UpdateAt,
        Name = deleteMiner.Name,
        Schedule = '0 0 * * *',
        IsActive = False,
        Id = deleteMiner.Id,
        InputTables = deleteMiner.InputTables,
        RecursiveRange = deleteMiner.RecursiveRange,
        GetInputs = deleteMiner.GetInputs,
        Formula = deleteMiner.Formula,
        IsSuccess = deleteMiner.IsSuccess
    )
    await minerService.update([_deleteMiner])
    addAudit = Audit(
        Id = 0,
        UserId = current_user.Id,
        ActionId = 2,
        ActionAt = datetime.datetime.now().strftime('%Y/%m/%d/'),
        MinerId = deleteMiner.Id
    )
    await auditService.add([addAudit])
    return True

@router.post("/createdefault")
async def create_default(newMiner: NewMiner, current_admin: User = Depends(userService.get_current_user_is_admin)):
    addMiner = Miner(
        DefineUserId = current_admin.Id,
        UserCanUse = 'all',
        CreateAt = datetime.datetime.now().strftime('%Y/%m/%d/'),
        UpdateAt = datetime.datetime.now().strftime('%Y/%m/%d/'),
        Name = newMiner.Name,
        Schedule = '0 0 * * *',
        InputTables = newMiner.InputTables,
        RecursiveRange = newMiner.RecursiveRange,
        GetInputs = newMiner.GetInputs,
        Formula = newMiner.Formula,
        IsActive = True,
        IsSuccess = True,
        Id = 0
    )
    addedMiner = await minerService.add([addMiner])
    return addedMiner

@router.post("/updatedefault")
async def update_default(updateMiner: Miner, current_admin: User = Depends(userService.get_current_user_is_admin)):
    _updateMiner = Miner(
        DefineUserId = current_admin.Id,
        UserCanUse = 'all',
        CreateAt = updateMiner.CreatAt,
        UpdateAt = datetime.datetime.now().strftime('%Y/%m/%d/'),
        Name = updateMiner.Name,
        Schedule = '0 0 * * *',
        IsActive = True,
        Id = updateMiner.Id,
        InputTables = updateMiner.InputTables,
        RecursiveRange = updateMiner.RecursiveRange,
        GetInputs = updateMiner.GetInputs,
        Formula = updateMiner.Formula,
        IsSuccess = updateMiner.IsSuccess
    )
    await minerService.update([_updateMiner])
    return True

@router.post("/deletedefault")
async def delete_default(deleteMiner: Miner, _: User = Depends(userService.get_current_user_is_admin)):
    deleteMiner.IsActive = False
    await minerService.update([deleteMiner])
    return True