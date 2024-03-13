FROM python:3.10-slim as base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV POETRY_NO_INTERACTION=1
ENV POETRY_VIRTUALENVS_CREATE=0
ENV POETRY_VERSION=1.8.2

RUN pip install pipx && pipx ensurepath && pipx install poetry==$POETRY_VERSION

FROM base as service

WORKDIR /app

COPY poetry.lock pyproject.toml ./

RUN pipx run poetry install -vvv

COPY . ./

ENTRYPOINT ["pipx", "run", "poetry", "run"]
