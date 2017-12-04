FROM python:2.7.14-slim-jessie

# Install gcc, required to compile bcrypt
RUN apt-get update && \
    apt-get install -y gcc

RUN mkdir /app
WORKDIR /app

# Install python libraries
ADD requirements.txt /app
RUN pip install -r requirements.txt

# Copy the rest of the code
ADD . /app

EXPOSE 5000

CMD [ "python", "server.py" ]
