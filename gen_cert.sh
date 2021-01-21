#!/bin/bash

WEBHOOK_HOST=$(grep WEBHOOK_HOST .env | cut -d '=' -f2)
openssl req -newkey rsa:2048 -sha256 -nodes -keyout cert/webhook_pkey.pem -x509 -days 365 -out cert/webhook_cert.pem -subj "/C=US/ST=New York/L=Brooklyn/O=Example Brooklyn Company/CN=$WEBHOOK_HOST"
