FROM python:3.7

WORKDIR /opt

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt