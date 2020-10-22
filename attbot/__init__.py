import flask
import os

from dotenv import load_dotenv
from attbot.worker import Worker
from attbot.db import DatabaseClient
from attbot.bot import bot, bot_bp, push_message, WEBHOOK_PATH

load_dotenv()
WEBHOOK_HOST = os.getenv('WEBHOOK_HOST')
WEBHOOK_PORT = os.getenv('WEBHOOK_PORT')
WEBHOOK_LISTEN = os.getenv('WEBHOOK_LISTEN')
WEBHOOK_URL = f'https://{WEBHOOK_HOST}:{WEBHOOK_PORT}/{WEBHOOK_PATH}'
WEBHOOK_SSL_CERT = 'cert/webhook_cert.pem'
WEBHOOK_SSL_PRIV = 'cert/webhook_pkey.pem'


def create_app():
    app = flask.Flask(__name__)
    app.register_blueprint(bot_bp)
    db_client = DatabaseClient.get_instance()

    # bot.remove_webhook()
    # bot.set_webhook(url=WEBHOOK_URL, certificate=open(WEBHOOK_SSL_CERT, 'r'))

    query_worker = Worker(push_message)
    query_worker.start()
    return app
