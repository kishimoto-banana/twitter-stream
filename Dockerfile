FROM python:3.10-slim

WORKDIR /app

RUN apt update && apt install -y --no-install-recommends build-essential libssl-dev libffi-dev python-dev

RUN pip install poetry==1.1.4

COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root --no-dev

COPY ./src ./src
