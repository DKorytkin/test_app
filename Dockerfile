FROM python:3.6-alpine

WORKDIR app
ARG DEV

RUN apk add --update \
    --virtual build-deps gcc musl-dev postgresql-dev \
    python3 python3-dev

COPY requirements.txt /app/requirements.txt
COPY requirements-dev.txt /app/requirements-dev.txt

RUN pip install -r /app/requirements.txt
RUN if [ $DEV ]; then pip install -r requirements-dev.txt; fi

COPY . /app
