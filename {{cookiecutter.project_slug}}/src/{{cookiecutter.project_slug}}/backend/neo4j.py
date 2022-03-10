import logging

from {{cookiecutter.project_slug}}.config import settings
from {{cookiecutter.project_slug}}.schemas import Document
from tenacity import (after_log, before_log, retry, stop_after_attempt,
                      wait_fixed)

from neo4j import GraphDatabase

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

max_tries = 60 * 5  # 5 minutes
wait_seconds = 1

class Documents:
    def __init__(self):
        self.driver = None

    @retry(
        stop=stop_after_attempt(max_tries),
        wait=wait_fixed(wait_seconds),
        before=before_log(logger, logging.INFO),
        after=after_log(logger, logging.WARN)
    )
    def init(self):
        self.driver = GraphDatabase.driver(settings.neo4j_url, auth=(settings.neo4j_user, settings.neo4j_password))

    def create_document(self, document: Document):
        with self.driver.session() as session:
            session.write_transaction(self._create_document, document)

    def add_entities(self, content: str, entities):
        if not self.driver:
            self.init()
        with self.driver.session() as session:
            session.write_transaction(self._add_entities, content, entities)

    @staticmethod
    def _create_document(tx, document: Document):
        tx.run("MERGE (a:Document {content: $content, title: $title})", content=document.content, title=document.title)

    @staticmethod
    def _add_entities(tx, content: str, entities):
        for entity in entities:
            tx.run("MERGE (entity:" + entity.label_ + " {text: $text})", text=entity.text)
            tx.run(
                "MATCH (document:Document {content: $content}), (entity:" 
                + entity.label_ 
                + " {text: $text}) MERGE (document)-[:SPAN {start: $start, end: $end}]->(entity)",
                content=content,
                text=entity.text,
                start=entity.start_char,
                end=entity.end_char
            )

documents = Documents()
