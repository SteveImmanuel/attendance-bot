import telebot
import logging
import os

from dotenv import load_dotenv
from worker import Worker

load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')

bot = telebot.TeleBot(API_TOKEN)
logger = telebot.logger.setLevel(logging.INFO)

@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, '/subscribe to get notification')

@bot.message_handler(func=lambda message: True)
def echo(message):
    bot.reply_to(message,message.text)

def push_message(chat_id):
    bot.send_message(chat_id, 'test push')

if __name__ == "__main__":
    query_worker = Worker(push_message)
    query_worker.start()
    bot.polling()