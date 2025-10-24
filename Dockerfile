FROM python:3.10-bullseye
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN mkdir -p code

WORKDIR code

CMD ["sh", "run-app-docker.sh"]
