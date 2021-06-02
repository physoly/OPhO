# syntax=docker/dockerfile:1

FROM python:3.9.5-slim-buster

WORKDIR /docker_app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

CMD ["python3", "run.py"]