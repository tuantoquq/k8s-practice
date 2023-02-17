from pydantic import BaseSettings
import os
from dotenv import load_dotenv

class Settings(BaseSettings):
    load_dotenv()
    started_year = 1956
    algorithm = "HS256"
    expire_minutes = 90
    secret = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"

    db_username = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASS')
    db_name = os.getenv('DB_NAME')
    db_host = os.getenv('DB_HOST')

    airflow_dag_folder = os.getenv('DAGS_FOLDER')