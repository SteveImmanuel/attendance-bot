import threading
import time
import os
import pytz
from datetime import datetime
from telebot import logger

from attbot.db import DatabaseClient
from attbot.messages import NOTIF


class Worker(threading.Thread):
    def __init__(self, callback):
        threading.Thread.__init__(self)
        self.callback = callback
        self.tz = pytz.timezone(os.getenv('TZ'))
        self.db_client = DatabaseClient.get_instance()
        self.current_day = datetime.now(self.tz).weekday()
        self.last_day = datetime.now(self.tz).weekday()

    def run(self):
        logger.info('Worker: Initializing database')
        self.db_client.exec_sql_file('attbot/telebot.db')
        logger.info('Worker: Database initialization success')

        while True:
            logger.info('Worker: Querying Database')
            event = self.db_client.get_current_events()
            
            if event:
                event_name = event[1]
                users = self.db_client.get_all_subscribed_users()
                users = [user[0] for user in users]

                logger.info('Worker: Sending notification to all subscribed users')
                for user in users:
                    self.callback(user, NOTIF.format(event_name))

                self.db_client.set_event_sent(event)
                logger.info('Worker: Successfully processed event')

            else:
                logger.info('Worker: No ongoing event')

            self.current_day = datetime.now(self.tz).weekday()
            if self.current_day != self.last_day:
                logger.info('Worker: Day changed, resetting all event')
                self.last_day = self.current_day
                self.db_client.reset_all_events()
            
            time.sleep(int(os.getenv('SLEEP_INTERVAL')))