FROM python:2.7.14-slim-jessie

RUN apt-get update && apt-get install -y gcc unixodbc-dev

RUN mkdir /app
WORKDIR /app

# Install python libraries
ADD requirements.txt /app
RUN pip install -r requirements.txt
