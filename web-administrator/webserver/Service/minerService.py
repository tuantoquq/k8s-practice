from Repository.minerRepository import MinerRepository
from Entity.entity import *
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from jinja2 import Template
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
import jinja2
import json
from Service.airflowService import AirflowService

reusable_oauth2 = HTTPBearer(
    scheme_name='Authorization'
)


class MinerService:
    def __init__(self, ):
        self.connector = MinerRepository()
        self.settings = Settings()
        self.airflow_service = AirflowService()

    def create_user_input_json(self, miner: Miner):
        indicator_name_upper = miner.Name.upper()
        indicator_name_upper = indicator_name_upper.replace("-", "").replace("_", "")
        user_input_dict = {"input_tables": miner.InputTables, "indicator_name": miner.Name,
                           "indicator_name_upper": indicator_name_upper,
                           "recursive_range": miner.RecursiveRange, "get_inputs_method": miner.GetInputs,
                           "formula_method": miner.Formula}

        with open(f"user_miner_input/{miner.Name}_user_input.json", "w") as json_file:
            json.dump(user_input_dict, json_file)

        with open(f"user_miner_input/{miner.Name}_user_input.json", "r") as json_file:
            return json_file.read()

    def get_task_template(self):
        with open(f"jinja_templates/airflow_task_template.py", "r") as task_template:
            return task_template.read()

    def get_miner_template(self):
        with open(f"jinja_templates/miner_template.py", "r") as miner_template:
            return miner_template.read()

    def save_miner_class(self, content, miner):
        with open(f"custom_miners/{miner.Name}_miner.py", "w") as miner_class_file:
            miner_class_file.write(content)

    def build_miner_class(self, miner):
        input_data = json.loads(self.create_user_input_json(miner))
        miner_template = Template(self.get_miner_template())
        miner_content = miner_template.render(**input_data)
        self.save_miner_class(miner_content, miner)

    def build_new_dag(self, miner):
        dag_content = self.airflow_service.get_src_code_by_id("indicator_dag")

        print("GET DAG CONTENT")

        class_init, task_init, dag_define = dag_content.split("# SECTION")

        # Add new class to DAG file
        with open(f"custom_miners/{miner.Name}_miner.py", "r") as miner_class_file:
            miner_class_str = miner_class_file.read()

            class_init += "\n" + miner_class_str

        # Add new Airflow Task
        input_data = json.loads(self.create_user_input_json(miner))
        task_template = Template(self.get_task_template())
        task_content = task_template.render(**input_data)

        task_init += "\n" + task_content

        # Add new DAG define
        input_tables_dict = json.loads(miner.InputTables)
        input_tables_list = list(input_tables_dict.keys())

        input_tables_list.remove("ticker_data") if "ticker_data" in input_tables_dict else None

        input_tables_str = "\n[" + ", ".join(input_tables_list) + "]" if len(input_tables_list) > 0 else ""
        new_dag_relation = input_tables_str + " >> " + "{indicator_name}_task".format(indicator_name=miner.Name) \
            if input_tables_str != "" else "{indicator_name}_task".format(indicator_name=miner.Name)
        dag_define += "\n" + new_dag_relation

        new_dag_content = class_init + "\n # SECTION\n" + task_init + "\n # SECTION\n" + dag_define

        # Delete old DAG
        self.airflow_service.delete_dag_by_id("indicator_dag")

        # Create new DAG
        with open("/Users/sonmt/HUST/2022-1/DATN-CN/src/Miners/dags/miner_dag.py", "w") as new_dag_file:
            new_dag_file.write(new_dag_content)

    async def add(self, miners: List[Miner]):
        miner = miners[0]
        # Update MySQL
        id_ = random.randint(100000, 1000000)
        while len(await self.connector.get_miner_by_id(id_)) > 0:
            id_ = random.randint(100000, 1000000)
        miner.Id = id_

        # Create miner class file
        self.build_miner_class(miner)

        # Create DAG file
        self.build_new_dag(miner)

        return await self.connector.insert(miners)

    async def update(self, miners: List[Miner]):
        return await self.connector.update(miners)

    async def delete(self, ids: List[str]):
        return await self.connector.delete(ids)

    async def get_all(self):
        return await self.connector.get_all()

    async def get_by_user_id(self, userId: int):
        return await self.connector.get_miner_by_user_id(userId)