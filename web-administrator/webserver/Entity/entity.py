from typing import Dict, List, Optional, Text, Union
from pydantic import BaseModel
from datetime import datetime


class User(BaseModel):
    Id: int
    Name: str
    Username: str
    Password: str
    Role: int  # 0 is admin, 1 is user
    IsActive: bool


class Miner(BaseModel):
    Id: int
    DefineUserId: int
    UserCanUse: str
    CreateAt: str
    UpdateAt: str
    Name: str
    Schedule: str
    Formula: str
    IsActive: bool
    InputTables: str = None
    RecursiveRange: int = None
    GetInputs: str = None
    IsSuccess: bool = None


class Audit(BaseModel):
    Id: int
    UserId: int
    ActionId: int  # 0 is create, 1 is update, 2 is delete
    ActionAt: str
    MinerId: int


class AuditResponse(BaseModel):
    Id: int
    UserId: int
    ActionId: int
    ActionAt: str
    MinerId: int
    Name: str
    Username: str
    MinerName: str


class MinerResponse(BaseModel):
    Id: int
    DefineUserId: int
    UserCanUse: str
    CreateAt: str
    UpdateAt: str
    Name: str
    Schedule: str
    Formula: str
    IsActive: bool
    Username: str
    NameDefineUser: str
    InputTables: str = None
    RecursiveRange: int = None
    GetInputs: str = None
    IsSuccess: bool = None
