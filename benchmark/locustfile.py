from locust import HttpUser, task

class LoadBenchmark(HttpUser):
    @task
    def fetch_products(self):
        res = self.client.post("/user/login", json={"Username": "tuannha","Password": "123456","Role": 1})
        print(res.json())