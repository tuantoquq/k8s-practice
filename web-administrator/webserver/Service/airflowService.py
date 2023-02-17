import requests
from requests.auth import HTTPBasicAuth

AIRFLOW_HOST = "http://localhost"
AIRFLOW_PORT = 8080
AIRFLOW_LIST_DAGS_ENDPOINT = "/api/v1/dags"
AIRFLOW_DAG_BY_ID_ENDPOINT = "/api/v1/dags/{dag_id}"
AIRFLOW_GET_SOURCE_CODE_ENDPOINT = "/api/v1/dagSources/{file_token}"
AIRFLOW_DELETE_DAG_BY_ID = ""


class AirflowService:
    def __init__(self):
        self.airflow_url = AIRFLOW_HOST + ":" + str(AIRFLOW_PORT)

    def get_list_dags(self):
        list_dags = requests.get(self.airflow_url + AIRFLOW_LIST_DAGS_ENDPOINT,
                                 auth=HTTPBasicAuth('airflow', 'airflow')).json()
        print(list_dags)

    def get_file_token_by_id(self, dag_id: str):
        dag_info = requests.get(self.airflow_url + AIRFLOW_DAG_BY_ID_ENDPOINT.format(dag_id=dag_id),
                                auth=HTTPBasicAuth('airflow', 'airflow')).json()
        return dag_info['file_token']

    def get_src_code_by_token(self, file_token: str):
        source_code = requests.get(self.airflow_url + AIRFLOW_GET_SOURCE_CODE_ENDPOINT.format(file_token=file_token),
                                   auth=HTTPBasicAuth('airflow', 'airflow'))
        return source_code.text

    def get_src_code_by_id(self, dag_id: str):
        file_token = self.get_file_token_by_id(dag_id)
        src_code = self.get_src_code_by_token(file_token)
        return src_code

    def delete_dag_by_id(self, dag_id: str):
        print(self.airflow_url + AIRFLOW_DAG_BY_ID_ENDPOINT.format(dag_id=dag_id))
        response = requests.delete(self.airflow_url + AIRFLOW_DAG_BY_ID_ENDPOINT.format(dag_id=dag_id),
                                   auth=HTTPBasicAuth('airflow', 'airflow'))
        return response


if __name__ == '__main__':
    airflow_service = AirflowService()
    # airflow_service.delete_dag_by_id("indicator_dag")
    airflow_service.get_list_dags()