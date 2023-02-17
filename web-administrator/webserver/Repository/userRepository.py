import mysql.connector
import sys
sys.path.append('../')
from config import Settings
from Entity.entity import *
from fastapi import HTTPException
from typing import List, Optional
import time

class UserRepository:
    def __init__(self, ):
        self.config = Settings()
        self.sql_insert = "INSERT INTO User (Id, Name, Username, Password, Role, IsActive) VALUES (%s,%s, %s, %s, %s, %s)"
        self.sql_update = "UPDATE User SET Name=%s, Password=%s, IsActive=%s WHERE Id = %s"
    
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
            raise HTTPException(status_code=422, detail="Failed to update record to database rollback: {}".format(error))
        mycursor.close()
        db.close()

    async def lock(self, Id, status):
        db = mysql.connector.connect(
                                    host="localhost",
                                    user=self.config.db_username,
                                    password=self.config.db_password,
                                    database=self.config.db_name
                                    )     
        mycursor = db.cursor()
        try:
            mycursor.executemany("UPDATE User SET IsActive = %s WHERE Id = %s",[(status,Id)])
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
        return True

    async def get_user_by_id(self, Id: str):
        db = mysql.connector.connect(
                                    host="localhost",
                                    user=self.config.db_username,
                                    password=self.config.db_password,
                                    database=self.config.db_name
                                    )     
        mycursor = db.cursor()
        mycursor.execute("select * from User where Id=%s",(Id,))
        try:
            records = mycursor.fetchall()
        except:
            mycursor.close()
            db.close()
            return []
        results = []
        for row in records:
            row = list(row)
            results.append(User(
                Id = row[0],
                Name =row[1],
                Username =row[2],
                Password =row[3],
                Role =row[4],
                IsActive =row[5]
            ))
        mycursor.close()
        db.close()
        return results

    async def get_user_by_user_name(self, Username: str):
        db = mysql.connector.connect(
                                    host="localhost",
                                    user=self.config.db_username,
                                    password=self.config.db_password,
                                    database=self.config.db_name
                                    )     
        mycursor = db.cursor()
        mycursor.execute("select * from User where Username=%s",(Username,))
        try:
            records = mycursor.fetchall()
        except:
            mycursor.close()
            db.close()
            return []
        results = []
        for row in records:
            row = list(row)
            results.append(User(
                Id = row[0],
                Name =row[1],
                Username =row[2],
                Password =row[3],
                Role =row[4],
                IsActive =row[5]
            ))
        mycursor.close()
        db.close()
        return results

    async def insert(self, users: List[User]):
        userAppend = []
        for user in users:
            try:
                if self.validate(user):
                    userAppend.append(user)                  
            except:
                raise HTTPException(status_code = 422, detail = "Username is used!")
        userAppend = [self.object2data(x) for x in userAppend]
        if len(userAppend):
            self.do_query(userAppend, self.sql_insert)
        return True

    def object2data(self, user: User):
        user = user.dict()
        user = tuple(list(user.values()))
        return user

    def validate(self, user:User):
        db = mysql.connector.connect(
                                    host="localhost",
                                    user=self.config.db_username,
                                    password=self.config.db_password,
                                    database=self.config.db_name
                                    )     
        mycursor = db.cursor()
        mycursor.execute("select * from User where Username=%s",(user.Username,))
        try:
            records = mycursor.fetchall()
            if (len(records) > 0):
                raise HTTPException(status_code=422, detail="Username is used!")
        except:
            mycursor.close()
            db.close()
            raise HTTPException(status_code=422, detail="Disconnect database")
        return True

    def do_query(self, users: List[tuple], sql_other:str):   
        db = mysql.connector.connect(
                                    host="localhost",
                                    user=self.config.db_username,
                                    password=self.config.db_password,
                                    database=self.config.db_name
                                    )     
        mycursor = db.cursor()
        try:
            mycursor.executemany(sql_other, users)
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