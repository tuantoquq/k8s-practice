import requests
from requests.auth import HTTPBasicAuth
from config import Settings


class AirflowService:
    def __init__(self):
        self.airflow_url = Settings().AIRFLOW_URL

    def get_list_dags(self):
        list_dags = requests.get(self.airflow_url + Settings().AIRFLOW_LIST_DAGS_ENDPOINT,
                                 auth=HTTPBasicAuth('airflow', 'airflow')).json()
        return list_dags

    def get_file_token_by_id(self, dag_id: str):
        dag_info = requests.get(self.airflow_url + Settings().AIRFLOW_DAG_BY_ID_ENDPOINT.format(dag_id=dag_id),
                                auth=HTTPBasicAuth('airflow', 'airflow')).json()
        return dag_info['file_token']

    def get_src_code_by_token(self, file_token: str):
        source_code = requests.get(self.airflow_url + Settings().AIRFLOW_GET_SOURCE_CODE_ENDPOINT.format(file_token=file_token),
                                   auth=HTTPBasicAuth('airflow', 'airflow'))
        return source_code.text

    def get_src_code_by_id(self, dag_id: str):
        file_token = self.get_file_token_by_id(dag_id)
        src_code = self.get_src_code_by_token(file_token)
        return src_code

    def delete_dag_by_id(self, dag_id: str):
        print(self.airflow_url + Settings().AIRFLOW_DAG_BY_ID_ENDPOINT.format(dag_id=dag_id))
        response = requests.delete(self.airflow_url + Settings().AIRFLOW_DAG_BY_ID_ENDPOINT.format(dag_id=dag_id),
                                   auth=HTTPBasicAuth(Settings().AIRFLOW_USER, Settings().AIRFLOW_PASS))
        return response