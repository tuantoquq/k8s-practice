import mysql.connector
import sys
sys.path.append('../')
from config import Settings
from Entity.entity import *
from fastapi import HTTPException
from typing import List, Optional
import time

class AuditRepository:
    def __init__(self, ):
        self.config = Settings()
        self.sql_insert = "INSERT INTO Audit (Id, UserId, ActionId, ActionAt, MinerId) VALUES (%s, %s, %s, %s, %s)"

    def object2data(self, audit: Audit):
        audit = audit.dict()
        audit = tuple(list(audit.values()))
        return audit
    
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

    def do_query(self, audits: List[tuple], sql_other:str):   
        db = mysql.connector.connect(
                                    host=self.config.db_host,
                                    user=self.config.db_username,
                                    password=self.config.db_password,
                                    database=self.config.db_name
                                    )     
        mycursor = db.cursor()
        try:
            mycursor.executemany(sql_other, audits)
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

    async def insert(self, audits: List[Audit]):
        auditAppend = []
        for audit in audits:            
            auditAppend.append(audit)              
        auditAppend = [self.object2data(x) for x in auditAppend]
        if len(auditAppend):
            self.do_query(auditAppend, self.sql_insert)
        return True

    async def get_all(self):        
        sql = "Select * from Audit inner join User on Audit.UserId = User.Id inner join Miner on Miner.Id = Audit.MinerId"
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
            results.append(AuditResponse(
                Id = row[0],
                ActionId =row[1],
                ActionAt =str(row[2]),
                UserId =row[3],
                MinerId = row[4],
                Name = row[6],
                Username = row[7],
                MinerName = row[16]
            ))
        mycursor.close()
        db.close()
        return results
    
    async def get_audit_by_id(self, Id: str):
        db = mysql.connector.connect(
                                    host=self.config.db_host,
                                    user=self.config.db_username,
                                    password=self.config.db_password,
                                    database=self.config.db_name
                                    )     
        mycursor = db.cursor()
        mycursor.execute("select * from Audit where Id=%s",(Id,))
        try:
            records = mycursor.fetchall()
        except:
            mycursor.close()
            db.close()
            return []
        results = []
        for row in records:
            row = list(row)
            results.append(Audit(
                Id = row[0],
                ActionId =row[1],
                ActionAt =row[2],
                UserId =row[3]
            ))
        mycursor.close()
        db.close()
        return results