from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import sqlalchemy as db

DB_USER = os.getenv('DB_USER', 'root')
DB_PASS = os.getenv('DB_PASS', 'Admin123**')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '3306')
DB_NAME = os.getenv('DB_NAME', 'manager')

DB_URL = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = db.create_engine(url=DB_URL)
connection = engine.connect()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/hello")
async def sample_get():
    test_table = db.Table('test',db.MetaData(), autoload=True, autoload_with=engine)
    sample_records = db.select(test_table)
    data = connection.execute(sample_records).fetchall()
    return {"status": 0, "message": "Successfully!", "data": data}
