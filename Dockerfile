FROM python:3.11-slim-buster

ENV PYTHONUNBUFFERED=1
ENV PATH="/root/.local/bin:$PATH"
ENV PYTHONPATH='/'

COPY ./poetry.lock /
COPY ./pyproject.toml /

RUN apt-get update -y && apt-get install curl -y \
&& curl -sSL https://install.python-poetry.org | python3 - \
&& /root/.local/bin/poetry config virtualenvs.create false \
&& /root/.local/bin/poetry install --no-root --no-interaction --no-ansi \
&& apt-get remove curl -y \
&& apt-get autoremove -y \
&& rm -rf /var/lib/apt/lists/*

COPY ./app /app
WORKDIR /app