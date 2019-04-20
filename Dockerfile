FROM python:3.7

ENV PYTHONUNBUFFERED 1

RUN mkdir /delservice

WORKDIR /delservice

ADD . /delservice/

RUN pip install -r requirements.txt
