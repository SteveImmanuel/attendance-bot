# Attendance Bot
Simple telegram bot to remind checking attendance. Personally helpful because since all classes become online during corona pandemic, so are all classes attendance. Build using python and implements multithreading.

## Available Commands
- `/start`, shows welcome message
- `/help`, shows how to use
- `/subscribe`, register to receive all notifications
- `/unsubscribe`, unregister to remove all notifications
- `/once`, register a one-time event with format. The format is `/once <event_name> <event_time>`. `<event_name>` can be a long string, while `<event_time>` must be in HH:MM 24-hour clock format
All the messages can be configured. See `Configuration` section.

## Configurations
In order to use this bot, first configure the environment variables. See the `.env.example` file.
- `API_TOKEN`, fill it with your Telegram API Token you generated. See <a href=https://core.telegram.org/bots#6-botfather>here</a> to generate API Token.
- `DB_HOST`, `DB_USERNAME`, `DB_PORT` are predefined, please don't change the value.
- `DB_PASSWORD`, fill with the database password.
- `DB_NAME`, fill the database name you want to use.
- `DB_POOL_SIZE`, fill with the number of pooling connection you want. Recommended value is >= 2.
- `DB_POOL_NAME`, fill with the pool name. Can be anything.

To configure the bot messages, open the `messages.py` file in the `attbot` directory and make all the changes.

Right now, all the events are still hardcoded in the database. You can insert or delete them by changing the `init.sql` file in the `db` directory. Just make sure you don't change the schema.

## Deployment
First make sure you have docker and docker-compose installed on your machine since it will make this process very easy.
1. Go to the root directory and type this in terminal.
```
cp .env.example .env
```
2. Fill out the .env file according to the `Configurations` guidelines.
3. Build the docker image.
```
docker-compose build
```
4. Finally start the service.
```
docker-compose up -d
```
Wait for a couple minutes. If all goes well, you should be able to interact with your telegram bot.

## Credits
Steve Immanuel 

September 2020