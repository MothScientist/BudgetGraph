FROM python:3.12.0

COPY requirements.txt /budget_control/
COPY app /budget_control/main
COPY app /budget_control/validators
COPY run.sh /budget_control/

WORKDIR /budget_control

RUN pip install -r requirements.txt

# Change working directory to /app/main
WORKDIR /budget_control/main

RUN python build_project.py && rm build_project.py

RUN rm create_db.sql

# Change back to /app
WORKDIR /budget_control

CMD ["sh", "./run.sh"]

EXPOSE 5000
