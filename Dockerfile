FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN mkdir /app

WORKDIR /app

COPY ./requirements.txt .

RUN pip3 install -r /app/requirements.txt --no-cache-dir

COPY . .
