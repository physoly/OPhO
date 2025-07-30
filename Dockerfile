# syntax=docker/dockerfile:1

FROM python:3.9-slim-bullseye

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      gcc \
      g++ \
      libpq-dev \
      python3-dev \
      build-essential && \
    rm -rf /var/lib/apt/lists/*


WORKDIR /docker_app

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . .

CMD ["python3", "run.py"]