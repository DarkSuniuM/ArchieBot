# ArchieBot
A Telegram bot to prevent spamming ads by MTProto (CLI) and API Bots.

## Setup
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
- Put automated file into a scheduled job runner like `crontab` so it can delete old messages.
