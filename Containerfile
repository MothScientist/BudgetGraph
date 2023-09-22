FROM python:alpine

COPY requirements.txt /app/

COPY main /app/main

COPY run.sh /app/

WORKDIR /app

RUN pip install -r requirements.txt

CMD ["sh", "./run.sh"]
#EXPOSE 8000

