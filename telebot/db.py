import mysql.connector

class DatabaseClient:
    def __init__(self):
        self.connector = mysql.connector.connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            password='root',
            database='telebot'
        )

        self.cursor = self.connector.cursor()

    def get_current_events(self):
        self.cursor.execute('SELECT * FROM users') 
        result = self.cursor.fetchall()
        return result