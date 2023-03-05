from Entity.entity import *
import json

TEMPLATES_FOLDER = "Jinja/jinja_templates/"
INPUT_FOLDER = "Jinja/user_miner_input/"
DRUID_SPEC_FOLDER = "Jinja/druid_spec/"
CUSTOM_MINERS_FOLDER = "Jinja/custom_miners/"


class Jinja2Service:
    def __init__(self):
        self.template_folder = TEMPLATES_FOLDER
        self.input_folder = INPUT_FOLDER
        self.druid_spec_folder = DRUID_SPEC_FOLDER
        self.custom_miners_folder = CUSTOM_MINERS_FOLDER

    def create_miner_input_json(self, miner: Miner):
        indicator_name_upper = miner.Name.upper()
        indicator_name_upper = indicator_name_upper.replace("-", "").replace("_", "")
        user_input_dict = {"input_tables": miner.InputTables, "indicator_name": miner.Name,
                           "indicator_name_upper": indicator_name_upper,
                           "recursive_range": miner.RecursiveRange, "get_inputs_method": miner.GetInputs,
                           "formula_method": miner.Formula}

        with open(f"{self.input_folder}{miner.Name}_user_input.json", "w") as json_file:
            json.dump(user_input_dict, json_file)

        with open(f"{self.input_folder}{miner.Name}_user_input.json", "r") as json_file:
            return json_file.read()

    def get_template(self, type: str):
        if type == "miner":
            with open(f"{self.template_folder}miner_template.py", "r") as miner_template:
                return miner_template.read()
        if type == "task":
            with open(f"{self.template_folder}airflow_task_template.py", "r") as task_template:
                return task_template.read()
        if type == "druid-spec":
            with open(f"{self.template_folder}druid_kafka_spec_template.json", "r") as task_template:
                return task_template.read()

    def save_miner_class(self, content, miner):
        with open(f"{self.custom_miners_folder}{miner.Name}_miner.py", "w") as miner_class_file:
            miner_class_file.write(content)

    def create_druid_spec(self, content, miner):
        with open(f"{self.druid_spec_folder}{miner.Name}_druid_kafka_spec.json", "w") as miner_class_file:
            miner_class_file.write(content)
        return f"{self.druid_spec_folder}{miner.Name}_druid_kafka_spec.json"