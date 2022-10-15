FROM python:3.10-alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY poetry.lock pyproject.toml /app/

RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev \
    && pip3 install poetry \
    && poetry install --no-interaction --no-ansi

COPY . /app/
