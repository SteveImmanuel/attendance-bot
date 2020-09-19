import telebot
import logging
import os

from dotenv import load_dotenv
from attbot.worker import Worker
from attbot.db import DatabaseClient
from attbot.messages import *

load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')
db_client = DatabaseClient.get_instance()
bot = telebot.TeleBot(API_TOKEN)
logger = telebot.logger.setLevel(logging.INFO)


@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, HELP)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, START)


@bot.message_handler(commands=['subscribe'])
def register_user(message):
    if db_client.add_user(message.chat.id):
        bot.send_message(message.chat.id, SUBSCRIBE_SUCC)
    else:
        bot.send_message(message.chat.id, SUBSCRIBE_FAIL)


@bot.message_handler(commands=['unsubscribe'])
def unregister_user(message):
    if db_client.remove_user(message.chat.id):
        bot.send_message(message.chat.id, UNSUB_SUCC)
    else:
        bot.send_message(message.chat.id, UNSUB_FAIL)


@bot.message_handler(func=lambda message: True)
def echo(message):
    bot.reply_to(message, message.text)


def push_message(chat_id, message):
    bot.send_message(chat_id, message)


if __name__ == "__main__":
    query_worker = Worker(push_message)
    query_worker.start()
    bot.polling()