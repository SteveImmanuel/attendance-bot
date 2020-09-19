#!/bin/bash

mysql --user $DB_USERNAME --password=$DB_PASSWORD $DB_NAME < telebot.db 