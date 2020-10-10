import os
import pytz
import re
import mysql.connector
from mysql.connector.errors import IntegrityError, OperationalError, ProgrammingError
from enum import Enum
from datetime import datetime


class DatabaseClient:
    __instance = None

    def __init__(self):
        if DatabaseClient.__instance is not None:
            raise Exception('Only allowed 1 instance')
        else:
            DatabaseClient.__instance = self
            self.connector = mysql.connector.connect(
                host=os.getenv('DB_HOST'),
                user=os.getenv('DB_USERNAME'),
                password=os.getenv('DB_PASSWORD'),
                port=int(os.getenv('DB_PORT')),
                database=os.getenv('DB_NAME'),
                pool_size=int(os.getenv('DB_POOL_SIZE')),
                pool_name=os.getenv('DB_POOL_NAME'))

            self.cursor = self.connector.cursor()
            self.tz = pytz.timezone(os.getenv('TZ'))

    def get_current_events(self):
        now = datetime.now(self.tz)
        result = []

        # hasn't handle intersecting event, assumes result always return 1 event
        query = 'SELECT id, event_name, \'regular\' FROM events WHERE day_of_week = %s AND start_time <= NOW() AND end_time >= NOW() AND has_sent = %s'
        self.cursor.execute(query, (now.weekday(), False))
        result = self.cursor.fetchall()

        ot_query = 'SELECT id, event_name, \'onetime\' FROM ot_events WHERE start_time <= NOW()'
        self.cursor.execute(ot_query)
        ot_result = self.cursor.fetchall()

        return [*result, *ot_result]

    def get_all_users(self):
        query = 'SELECT chat_id FROM users'
        self.cursor.execute(query)
        result = self.cursor.fetchall()

        return result

    def set_event_sent(self, event):
        event_id = event[0]
        query = 'UPDATE events SET has_sent = %s WHERE id = %s'
        self.cursor.execute(query, (True, event_id))
        self.connector.commit()

    def reset_all_events(self):
        query = 'UPDATE events SET has_sent = false'
        self.cursor.execute(query)
        self.connector.commit()

    def add_user(self, chat_id):
        try:
            query = 'INSERT INTO users VALUES (NULL, %s)'
            self.cursor.execute(query, (chat_id, ))
            self.connector.commit()
            return True
        except IntegrityError:
            return False

    def remove_user(self, chat_id):
        try:
            query = 'DELETE FROM users WHERE chat_id = %s'
            self.cursor.execute(query, (chat_id, ))
            self.connector.commit()
            return True
        except Exception:
            return False

    def add_ot_event(self, event_name, date_time):
        try:
            query = 'INSERT INTO ot_events VALUES (NULL, %s, %s)'
            self.cursor.execute(query, (event_name, date_time))
            self.connector.commit()
            return True
        except IntegrityError:
            return False

    def remove_ot_event(self, event):
        query = 'DELETE FROM ot_events WHERE id = %s'
        self.cursor.execute(query, (event[0], ))
        self.connector.commit()

    @staticmethod
    def get_instance():
        if DatabaseClient.__instance is None:
            DatabaseClient()
        return DatabaseClient.__instance