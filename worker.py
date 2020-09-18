import threading

import time

class Worker(threading.Thread):
    def __init__(self, callback):
        threading.Thread.__init__(self)
        self.callback = callback


    def run(self):
        print('querying db')
        self.check_database()
        print('done')


    def check_database(self):
        time.sleep(1)