FROM python:3.8.2-alpine

RUN apk update && apk add build-base python-dev py-pip jpeg-dev zlib-dev \
    openssl-dev gcc libffi-dev postgresql-dev autoconf automake alpine-sdk \
    libtool bash curl

WORKDIR /usr/src/app

COPY ./requirements.txt /usr/src/app

RUN pip install --upgrade --no-cache-dir pip
RUN pip install -r requirements.txt

COPY . /usr/src/app

WORKDIR /usr/src/app/hmac-server
