FROM python:3.10-bullseye
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt requirements.txt

RUN mkdir -p code

RUN python -m venv env_project

RUN env_project/bin/pip install -r requirements.txt
