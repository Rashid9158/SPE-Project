FROM python:3.7

ENV PYTHONUNBUFFERED 1

RUN mkdir /delservice

WORKDIR /delservice

ADD . /delservice/

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["/bin/bash", "-c", "python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
