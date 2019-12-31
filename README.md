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
0. Create a virtual environment using `virtualenv venv` inside the cloned directory.
0. Activate the virtual environment using `source venv/bin/activate`.
0. Install requirements using `pip install -r requirements.txt`.
0. Create a MariaDB/MySQL Database.
0. Rename `.env.example` to `.env` and fill in the data.
0. Migrate database to the latest version using `alembic upgrade head`.

### 2. Usage
- Run the `app.py` file, you can use something like `tmux` or `screen` to run it in background.


## Docker Setup
You can run this bot using Docker too!

### 1. How to Setup
0. Clone this repostiry
0. Go to the project's directory
0. Create a MariaDB/MySQL Database.
0. Rename `.env.example` to `.env` and fill in the data.
0. Build the docker image using `docker build . -t archie_bot`

### 2. Usage
0. Run the container using `docker run -d archie_bot`

