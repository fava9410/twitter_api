FROM python:3.7-alpine

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt

RUN apk add --no-cache --virtual .build-deps gcc musl-dev build-base
RUN pip install -r /requirements.txt
RUN apk del .build-deps gcc musl-dev build-base

RUN mkdir /app
WORKDIR /app
COPY ./app /app

ENTRYPOINT FLASK_APP=app.py flask run --host=0.0.0.0
EXPOSE 5000