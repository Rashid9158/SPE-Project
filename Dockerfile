FROM python:3.7-alpine

ENV PYTHONUNBUFFERED 1

COPY . .

RUN pip install -r requirements.txt
