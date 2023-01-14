from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import sqlalchemy as db
from pydantic import BaseModel 

DB_USER = os.getenv('DB_USER', 'root')
DB_PASS = os.getenv('DB_PASS', 'Admin123**')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '3306')
DB_NAME = os.getenv('DB_NAME', 'manager')

DB_URL = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = db.create_engine(url=DB_URL)
connection = engine.connect()
meta = db.MetaData()
users_table = db.Table('users', 
                meta, 
                db.Column('id', db.Integer, primary_key=True),
                db.Column('name', db.String(256)),
                db.Column('age', db.Integer),
                mysql_engine='InnoDB',
                mysql_charset='utf8')
meta.create_all(engine)

class User (BaseModel):
    name: str
    age: int

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/get-all")
async def get_all():
    sample_records = db.select(users_table)
    data = connection.execute(sample_records).fetchall()
    return {"status": 0, "message": "Get all user successfully!", "data": data}

@app.get("/get/{user_id}")
async def get_by_id(user_id: int):
    sample_records = db.select(users_table).where(users_table.c.id==user_id)
    data = connection.execute(sample_records).fetchone()
    return {"status": 0, "message": "Get user successfully!", "data": data}

@app.post("/create")
async def create(user: User):
    sql = (db.insert(users_table).values(name=user.name, age=user.age))
    connection.execute(statement=sql)
    return {"status": 0, "message": "Create user successfully!"}
        

@app.delete('/delete/{user_id}')
async def delete(user_id: int):
    sql = db.select(users_table).where(users_table.c.id==user_id)
    data = connection.execute(statement=sql).fetchone()
    if data is None:
        raise HTTPException(status_code=400, detail="User not found with input id")
    else: 
        sql = db.delete(users_table).where(users_table.c.id==user_id)
        connection.execute(statement=sql)
        return {"status": 0, "message": "Delete user successfully!"}