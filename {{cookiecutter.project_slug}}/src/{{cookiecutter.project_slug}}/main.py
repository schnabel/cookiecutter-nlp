''' minimal FastAPI template
'''
import asyncio
import time

import spacy
from fastapi import FastAPI

from {{cookiecutter.project_slug}}.backend import neo4j
from {{cookiecutter.project_slug}}.schemas import Document

from .er_worker import add_entities

app = FastAPI()
nlp = spacy.load("en_core_web_md")


@app.on_event("startup")
def startup():
    ''' simulate some slow startup task
    '''
    neo4j.documents.init()

@app.get("/status", summary="Get status", tags=["Status"])
async def status():
    ''' Checks if the service is running and operational.
    '''
    await asyncio.sleep(1)
    return {"status": "ready"}

@app.put("/documents", summary="Create document.", tags=["Documents"])
def create_document(document: Document):
    '''Create a document node in neo4j
    '''
    neo4j.documents.create_document(document)
    add_entities.delay(document.content)
