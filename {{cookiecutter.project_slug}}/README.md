# Entity recognition project
This project is intended to be a template for a NLP stack with a set of interesting tools/frameworks. It uses [spacy](https://spacy.io/), [neo4j](https://neo4j.com/), [fastapi](https://fastapi.tiangolo.com/) and [celery](https://docs.celeryproject.org/en/stable/index.html).

## Prerequisites
* python3.8 
* java (for gradle)
* [gradle-python-plugin](https://github.com/schnabel/python-plugin)
* docker (to be able to create docker images)
* minikube/kubernetes (to run a complete microservice stack for integration and load testing)

## Howto build/use the project
This project uses [gradle](https://gradle.org/) as build tool. I choose gradle because it allows to integrate different build aspects with one tools pretty easy. Thinks like incremental builds, testing, creating docker images and even spin up minikube to run the complete stack for load testing.

To see all possible gradle commands run:
``` bash
./gradlew tasks --all
```
