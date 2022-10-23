# syntax=docker/dockerfile:1

FROM python:3.10

WORKDIR /notifier

COPY requirements/requirements.txt requirements/requirements.txt
RUN pip3 install -r requirements/requirements.txt

COPY . .

ENV PYTHONPATH /notifier
CMD [ "python3", "src/main.py"]

