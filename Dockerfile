FROM python:3.10-slim-buster



ENV PYTHONUNBUFFERED=1



WORKDIR /usr/src/app


COPY ./requirements.txt .



RUN apt-get update && apt-get install -y libpq-dev build-essential \ 
    && pip install -r requirements.txt 

COPY ./src .