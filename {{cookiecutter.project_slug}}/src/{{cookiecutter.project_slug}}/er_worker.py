import spacy
from celery import Celery

from {{cookiecutter.project_slug}}.backend.neo4j import documents

app = Celery("worker", broker="amqp://guest@rabbitmq//", result_backend = 'rpc://')
nlp = spacy.load("en_core_web_md")


@app.task(ignore_result=True)
def add_entities(content: str):
    doc = nlp(content)
    documents.add_entities(content, doc.ents)
