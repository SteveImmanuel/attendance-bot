import threading
import time
import os
import pytz
from datetime import datetime
from telebot import logger

from attbot.db import DatabaseClient
from attbot.messages import NOTIF, OT_NOTIF


class Worker(threading.Thread):
    def __init__(self, callback):
        threading.Thread.__init__(self)
        self.callback = callback
        self.tz = pytz.timezone(os.getenv('TZ'))
        self.db_client = DatabaseClient.get_instance()
        self.current_day = datetime.now(self.tz).weekday()
        self.last_day = datetime.now(self.tz).weekday()

    def run(self):
        logger.info('Database connected')
        while True:
            events = self.db_client.get_current_events()

            if len(events) > 0:
                for event in events:
                    event_type = event[2]
                    event_name = event[1]
                    users = self.db_client.get_all_users()
                    users = [user[0] for user in users]

                    message = NOTIF if event_type == 'regular' else OT_NOTIF

                    logger.info('Sending notification to all subscribed users')
                    try:
                        for user in users:
                            self.callback(user, message.format(event_name))

                        if event_type == 'regular':
                            self.db_client.set_event_sent(event)
                        else:
                            self.db_client.remove_ot_event(event)
                        logger.info('Successfully processed event')
                    except Exception as e:
                        logger.error(str(e))

            else:
                logger.info('No ongoing event')

            self.current_day = datetime.now(self.tz).weekday()
            if self.current_day != self.last_day:
                logger.info('Day changed, resetting all event')
                self.last_day = self.current_day
                self.db_client.reset_all_events()

            time.sleep(int(os.getenv('SLEEP_INTERVAL')))