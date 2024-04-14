FROM python:3.12.2-alpine3.18

COPY requirements.txt run.sh  /main/
COPY app /main/app

WORKDIR /main

RUN apt-get update -y && apt-get upgrade -y && apt-get install -y openssl

RUN python -m pip install --upgrade pip && pip install -r requirements.txt

WORKDIR /main/app

RUN python build_project.py && rm build_project.py && rm create_db.sql

WORKDIR /main

CMD ["sh", "./run.sh"]

EXPOSE 5000
