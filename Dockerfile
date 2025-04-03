FROM python:3.13-alpine

WORKDIR /usr/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN apk update && apk add bash

COPY . .
VOLUME /usr/app/config

CMD ["python", "-u", "src/script.py"]