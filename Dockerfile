FROM python:3.8-alpine
WORKDIR /code
RUN pip install --upgrade pip
RUN apk add --no-cache \
        gcc \
        libressl-dev \
        musl-dev \
        libffi-dev
RUN pip install cryptography
RUN pip install requests
RUN pip install fastapi
RUN pip install uvicorn[standar]
RUN pip install peewee
RUN pip install pytest
RUN pip install pyjwt[crypto]
RUN pip install beautifulsoup4

#mysqlclient installation
RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add --no-cache mariadb-dev
RUN pip install mysqlclient
RUN apk del build-deps

COPY ./src/api/main.py ./code
EXPOSE 8889