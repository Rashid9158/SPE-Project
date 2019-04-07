FROM python:3.7-alpine

ENV PYTHONUNBUFFERED 1

COPY . .

RUN sudo apt install libjpeg-dev zlib1g-dev

RUN pip install -r requirements.txt
