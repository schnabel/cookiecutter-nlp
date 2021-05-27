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
Example commands:
``` bash
./gradlew pytest                ## run all pytests
./gradlew integrationTest       ## set up a complete application stack in minikube and run the tests against real dbs etc
./gradlew loadTest              ## set up a complete application stack in minikube and run load tests with locust
```

## View the entities detected with spacy in neo4j
* Get the ip of your minikube:
``` bash
minikube ip
```
* To use the neo4j UI, open http://minikube_ip:30474/ in your browser.
* Change the connect URL to port 30687 and type the password you choose when setting up the project (neo4j_change_me in case you did not change it :-)).
