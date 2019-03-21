# ArchieBot
A Telegram bot to prevent spamming ads by MTProto (CLI) and API Bots.

## Setup
### 1. Requirements
- Python 3.6+

### 2. How to setup
1. Clone repository.
1. Create a virtual environment using `virtualenv venv` inside the cloned directory.
1. Activate the virtual environment using `source venv/bin/activate`.
1. Install requirements using `pip install -r requirements.txt`.
1. Rename `.env.example` to `.env` and fill in the data.
1. Initialize the database using `python archie.py generate-db`.

### 3. Usage
- Run the `app.py` file, you can use something like `tmux` or `screen` to run it in background.
