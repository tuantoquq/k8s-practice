from Repository.auditRepository import AuditRepository
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
import random

reusable_oauth2 = HTTPBearer(
        scheme_name='Authorization'
    )
class AuditService:
    def __init__(self, ):
        self.connector = AuditRepository()
        self.settings = Settings()

    async def add(self, audits: List[Audit]):
        for audit in audits:
            id_ = random.randint(100000,1000000)
            while len(await self.connector.get_audit_by_id(id_)) > 0:
                id_ = random.randint(100000,1000000)
            audit.Id = id_
        return await self.connector.insert(audits)

    async def get_all(self):
        return await self.connector.get_all()