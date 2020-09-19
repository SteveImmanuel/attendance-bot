FROM python:3.8

COPY attbot /app/attendace-bot/attbot
COPY requirements.txt /app/attendace-bot

WORKDIR /app/attendace-bot
RUN pip install -r requirements.txt

ENV WAIT_VERSION 2.7.2
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/$WAIT_VERSION/wait /wait
RUN chmod +x /wait