FROM python:alpine3.15

ENV PYTHONUNBUFFERED=1
LABEL maintainer 0805004949

RUN addgroup app && adduser -SG app app
USER app
WORKDIR /app

COPY . /app
RUN python -m pip install --upgrade pip &&\
    pip install -r requirements.txt
   
