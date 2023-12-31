# syntax=docker/dockerfile:1

FROM python:3.13-rc-slim
LABEL authors="T306Dev"

EXPOSE 81
WORKDIR /python-docker

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "hypercorn", "main:app"]