# ArchieBot

A Telegram bot to prevent spamming ads by MTProto (CLI) and API Bots.

## Features

- Kick Bots (Not MTPRoto bots, but the accounts that Telegram identifies as bot)
- Preventing spammers by showing them a simple math equation as captcha
- Search in Archlinux's Wiki

## Normal Setup

### 0. Requirements

- Python 3.6+

### 1. How to setup

0. Clone repository.
1. Create a virtual environment using `virtualenv venv` inside the cloned directory.
2. Activate the virtual environment using `source venv/bin/activate`.
3. Install requirements using `pip install -r requirements.txt`.
4. Create a MariaDB/MySQL Database.
5. Rename `.env.example` to `.env` and fill in the data ([Configuration](#Configuration)).
6. Migrate database to the latest version using `alembic upgrade head`.

### 2. Usage

- Run the `app.py` file, you can use something like `tmux` or `screen` to run it in background.

## Docker Setup

You can run this bot using Docker too!

### 1. How to Setup

0. Clone this repostiry
1. Go to the project's directory
2. Create a MariaDB/MySQL Database.
3. Rename `.env.example` to `.env` and fill in the data ([Configuration](#Configuration)).
4. Build the docker image using `docker build . -t archie_bot`

### 2. Usage

0. Run the container using `docker run -d archie_bot`

## Configuration (.env helper)

|           Key           | Description                                                                                                       | Required | Example                                        |
| :---------------------: | ----------------------------------------------------------------------------------------------------------------- | :------: | ---------------------------------------------- |
|        BOT_TOKEN        | Bot's token from @BotFather                                                                                       |   Yes    | 1013037333:AAF3Fi_UeaLSGzmh50h8gArsoYLWwAp-OVI |
|        BOT_PROXY        | HTTP Proxy Leave empty to disable                                                                                 |    No    | http://127.0.0.1:1090                          |
| BOT_RECOVERY_CHANNEL_ID | A Channel to forward recoverable messages (Bot should be admin in this channel), Leave empty to disable           |    No    | -1001368511332                                 |
|         DB_URI          | Database URI for SQLAlchemy engine [READ MORE](https://docs.sqlalchemy.org/en/13/core/engines.html#database-urls) |   Yes    | mysql://user:password@127.0.0.1:3306/archie_db |
