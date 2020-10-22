FROM python:3.8

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY attbot /app/attendance-bot/attbot
COPY requirements.txt /app/attendance-bot
COPY cert /app/attendance-bot/cert

WORKDIR /app/attendance-bot
RUN pip install -r requirements.txt

ENV WAIT_VERSION 2.7.2
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/$WAIT_VERSION/wait /wait
RUN chmod +x /wait