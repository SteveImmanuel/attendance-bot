import telebot
import logging
import os

from datetime import datetime
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


@bot.message_handler(commands=['once'])
def remind_once(message):
    user_text = message.text
    user_text = user_text.split(' ')

    if len(user_text) >= 3:
        now = datetime.now()
        event_name = ' '.join(user_text[1:-1])
        str_time = user_text[-1]
        try:
            temp = datetime.strptime(str_time, '%H:%M')
            event_time = now.replace(hour=temp.hour,
                                     minute=temp.minute,
                                     second=0)
            if event_time > now:
                if db_client.add_ot_event(event_name, event_time):
                    bot.send_message(message.chat.id, OT_SUCCESS)
                else:
                    bot.send_message(message.chat.id, OT_FAIL)

            else:
                bot.send_message(message.chat.id, TIME_PASSED_ERROR)
        except Exception as e:
            telebot.logger.error(e)
            bot.send_message(message.chat.id, WRONG_TIME)
    else:
        bot.send_message(message.chat.id, WRONG_FORMAT)


def push_message(chat_id, message):
    bot.send_message(chat_id, message)


if __name__ == "__main__":
    query_worker = Worker(push_message)
    query_worker.start()
    bot.polling()