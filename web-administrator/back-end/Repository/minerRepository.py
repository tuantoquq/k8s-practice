import mysql.connector
import sys
sys.path.append('../')
from config import Settings
from Entity.entity import *
from fastapi import HTTPException
from typing import List, Optional
import time

class MinerRepository:
    def __init__(self, ):
        self.config = Settings()
        self.sql_insert = "INSERT INTO Miner (Id, DefineUserId, UserCanUse, CreateAt, UpdateAt, Name, Schedule, Formula, IsActive, InputTables, RecursiveRange, GetInputs, IsSuccess) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        self.sql_update = "UPDATE Miner set DefineUserId = %s, UserCanUse = %s, CreateAt = %s, UpdateAt = %s, Name = %s, Schedule = %s, Formula = %s, IsActive = %s, InputTables = %s, RecursiveRange = %s, GetInputs = %s, IsSuccess = %s WHERE Id= %s"

    def object2data(self, miner: Miner, id_place='first'):
        miner = miner.dict()
        miner = list(miner.values())
        if (id_place=='last'):
            minerId = miner[0]
            miner.pop(0)
            miner.append(minerId)
        return tuple(miner)
    
    async def do_query(self, sql_other:str):
        db = mysql.connector.connect(
                                    host=self.config.db_host,
                                    user=self.config.db_username,
                                    password=self.config.db_password,
                                    database=self.config.db_name
                                    )   
        mycursor = db.cursor()
        try:
            mycursor.execute(sql_other)
            db.commit()
        except mysql.connector.Error as error:
            print("Failed to update record to database rollback: {}".format(error))
            # reverting changes because of exception
            db.rollback()
            mycursor.close()
            db.close()
            raise HTTPException(status_code = 422, detail="Failed to update record to database rollback: {}".format(error))
        mycursor.close()
        db.close()

    async def do_query(self, miners: List[tuple], sql_other:str):   
        db = mysql.connector.connect(
                                    host=self.config.db_host,
                                    user=self.config.db_username,
                                    password=self.config.db_password,
                                    database=self.config.db_name
                                    )     
        mycursor = db.cursor()
        try:
            mycursor.executemany(sql_other, miners)
            db.commit()
        except mysql.connector.Error as error:
            print("Failed to update record to database rollback: {}".format(error))
    # reverting changes because of exception
            db.rollback()
            mycursor.close()
            db.close()
            raise HTTPException(status_code=422, detail="Failed to update record to database rollback: {}".format(error))
        mycursor.close()
        db.close()

    async def insert(self, miners: List[Miner]):
        minerAppend = []
        for miner in miners:            
            minerAppend.append(miner)              
        minerAppend = [self.object2data(x) for x in minerAppend]
        if len(minerAppend):
            await self.do_query(minerAppend, self.sql_insert)
        return minerAppend
    
    async def get_miner_by_id(self, Id: str):
        db = mysql.connector.connect(
                                    host=self.config.db_host,
                                    user=self.config.db_username,
                                    password=self.config.db_password,
                                    database=self.config.db_name
                                    )     
        mycursor = db.cursor()
        mycursor.execute("select * from Miner where Id=%s and IsActive=True",(Id,))
        try:
            records = mycursor.fetchall()
        except:
            mycursor.close()
            db.close()
            return []
        results = []
        for row in records:
            row = list(row)
            results.append(Miner(
                Id = row[0],
                DefineUserId = row[1],
                UserCanUse = row[2],
                CreateAt = str(row[3]),
                UpdateAt = str(row[4]),
                Name = row[5],
                Schedule = row[6],
                Formula = row[7],
                IsActive = row[8],
                InputTables = row[9],
                RecursiveRange = row[10],
                GetInputs = row[11],
                IsSuccess = row[12]
            ))
        mycursor.close()
        db.close()
        return results

    async def get_all(self):        
        sql = "SELECT * FROM Miner inner join User on Miner.DefineUserId = User.Id WHERE Miner.IsActive = True"
        db = mysql.connector.connect(
                                    host=self.config.db_host,
                                    user=self.config.db_username,
                                    password=self.config.db_password,
                                    database=self.config.db_name
                                    )
        mycursor = db.cursor()
        mycursor.execute(sql)
        try:
            records = mycursor.fetchall()
        except:
            mycursor.close()
            db.close()
            return []
        results = []
        for row in records:
            results.append(MinerResponse(
                Id = row[0],
                DefineUserId = row[1],
                UserCanUse = row[2],
                CreateAt = str(row[3]),
                UpdateAt = str(row[4]),
                Name = row[5],
                Schedule = row[6],
                Formula = row[7],
                IsActive = row[8],
                NameDefineUser = row[14],
                Username = row[15],
                InputTables = row[9],
                RecursiveRange = row[10],
                GetInputs = row[11],
                IsSuccess = row[12]
            ))
        mycursor.close()
        db.close()
        return results

    async def get_miner_by_user_id(self, UserId: str):
        db = mysql.connector.connect(
                                    host=self.config.db_host,
                                    user=self.config.db_username,
                                    password=self.config.db_password,
                                    database=self.config.db_name
                                    )     
        mycursor = db.cursor()
        mycursor.execute("select * from Miner where DefineUserId=%s and IsActive = True",(UserId,))
        try:
            records = mycursor.fetchall()
        except:
            mycursor.close()
            db.close()
            return []
        results = []
        for row in records:
            row = list(row)
            results.append(Miner(
                Id = row[0],
                DefineUserId = row[1],
                UserCanUse = row[2],
                CreateAt = str(row[3]),
                UpdateAt = str(row[4]),
                Name = row[5],
                Schedule = row[6],
                Formula = row[7],
                IsActive = row[8],
                InputTables = row[9],
                RecursiveRange = row[10],
                GetInputs = row[11],
                IsSuccess = row[12]
            ))
        mycursor.close()
        db.close()
        return results

    async def update(self,  miners: List[Miner]):
        miners = [self.object2data(x, 'last') for x in miners]
        await self.do_query(miners, self.sql_update)
        return True