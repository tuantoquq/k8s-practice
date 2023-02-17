import requests

url = "http://localhost:8080/api/v1/dags"
username = "airflow"
password = "airflow"
response = requests.get(url, auth=(username, password))
print(response.status_code)
print(response.json())