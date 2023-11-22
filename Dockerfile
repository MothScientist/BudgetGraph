FROM python:3.12.0

COPY requirements.txt /main/
COPY app /main/app
COPY run.sh /main/

WORKDIR /main

RUN pip install -r requirements.txt

# Change working directory to /app/app
WORKDIR /main/app

RUN python build_project.py && rm build_project.py

RUN rm create_db.sql

# Change back to /app
WORKDIR /main

CMD ["sh", "./run.sh"]

EXPOSE 5000
