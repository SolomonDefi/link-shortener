# BASE IMAGE (? MB)
# ------------------------------------------------------------------------------------
FROM python:3.9-slim-bullseye

ARG TINI_VER=0.19

ENV TINI_VER=$TINI_VER

WORKDIR /usr/src

RUN apt-get update && apt-get install -y gcc
RUN python -m pip install poetry
COPY . .
COPY .env.dist ./.env
RUN poetry install --no-dev && poetry run flask db upgrade

CMD ["poetry", "run", "python", "application.py"]
