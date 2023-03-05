from Repository.minerRepository import MinerRepository
from Entity.entity import *
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from jinja2 import Template
from config import Settings
from typing import List
from fastapi.security import HTTPBearer
import random
import json
from Service.airflowService import AirflowService
from Jinja.jinjaService import Jinja2Service

import requests

reusable_oauth2 = HTTPBearer(
    scheme_name='Authorization'
)


class MinerService:
    def __init__(self):
        self.connector = MinerRepository()
        self.settings = Settings()
        self.airflow_service = AirflowService()
        self.jinja2_service = Jinja2Service()

    def build_miner_class(self, miner):
        input_data = json.loads(self.jinja2_service.create_miner_input_json(miner))
        miner_template = Template(self.jinja2_service.get_template(type="miner"))
        miner_content = miner_template.render(**input_data)
        self.jinja2_service.save_miner_class(miner_content, miner)

    def build_new_dag(self, miner):
        dag_content = self.airflow_service.get_src_code_by_id("indicator_dag")

        print("GET DAG CONTENT")

        class_init, task_init, dag_define = dag_content.split("# SECTION")

        # Add new class to DAG file
        with open(f"custom_miners/{miner.Name}_miner.py", "r") as miner_class_file:
            miner_class_str = miner_class_file.read()

            class_init += "\n" + miner_class_str

        # Add new Airflow Task
        input_data = json.loads(self.jinja2_service.create_miner_input_json(miner))
        task_template = Template(self.jinja2_service.get_template(type="task"))
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
        with open(Settings.DAGS_FOLDER, "w") as new_dag_file:
            new_dag_file.write(new_dag_content)

    def build_and_send_druid_spec(self, miner):

        # Create Druid spec JSON data
        input_data = json.loads(self.jinja2_service.create_miner_input_json(miner))
        druid_spec_template = Template(self.jinja2_service.get_template(type="druid-spec"))
        druid_spec_content = druid_spec_template.render(**input_data)
        druid_spec_path = self.jinja2_service.create_druid_spec(druid_spec_content, miner)

        # Send Druid spec JSON data to Druid overlord
        headers = {'Content-Type': 'application/json'}
        with open(druid_spec_path, "r") as druid_spec_file:
            druid_spec_json = json.load(druid_spec_file)
        response = requests.post(f"{Settings().DRUID_OVERLORD}/druid/indexer/v1/supervisor", headers=headers, json=druid_spec_json).json()
        print(response)

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

        # Create Druid Kafka spec
        self.build_and_send_druid_spec(miner)

        return await self.connector.insert(miners)

    async def update(self, miners: List[Miner]):
        return await self.connector.update(miners)

    async def delete(self, ids: List[str]):
        return await self.connector.delete(ids)

    async def get_all(self):
        return await self.connector.get_all()

    async def get_by_user_id(self, userId: int):
        return await self.connector.get_miner_by_user_id(userId)