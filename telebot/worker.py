import threading
import time

from db import DatabaseClient

class Worker(threading.Thread):
    def __init__(self, callback):
        threading.Thread.__init__(self)
        self.callback = callback
        self.db_client = DatabaseClient()


    def run(self):
        print('querying db')
        result = self.db_client.get_current_events()
        print(result)


    def check_database(self):
        time.sleep(1)