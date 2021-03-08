FROM python:3.8

WORKDIR /usr/src/app

RUN pip install pipenv

COPY Pipfile* ./
RUN pipenv install
RUN pipenv run python -m spacy download en_core_web_md
COPY {{cookiecutter.project_slug}} ./{{cookiecutter.project_slug}}/

CMD [ "pipenv", "run", "uvicorn", "{{cookiecutter.project_slug}}.main:app", "--host", "0.0.0.0"]