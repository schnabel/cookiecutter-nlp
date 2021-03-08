import pandas as pd
from locust import HttpUser, between, task


class FooUser(HttpUser):
    wait_time = between(0, 2)

    @task
    def get_status(self):
        self.client.get("/status")

    @task
    def create_document(self):
        row = self.documents.sample(n=1)
        self.client.put("/documents", json={'title': row['title'].values[0], 'content': row['content'].values[0]})

    def on_start(self):
        self.documents = pd.read_csv("data/news.cvs.zip", usecols=["title", "content"])
