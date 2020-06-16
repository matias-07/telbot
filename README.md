# TelBot

Telegram chat bot built using the Telegram Bot API.

# Installation & Usage

1. Get a [Telegram Bot API](https://core.telegram.org/bots/api) token.
2. Set your token as a environment variable: `export TELEGRAM_API_TOKEN={your_token}`.
3. Clone this repository.
4. Inside the repository's folder: `python3 -m venv .` and then `source bin/activate`.
5. Install the requirements: `pip install -r requirements.txt`.
6. Run the bot: `python src/main.py`.

# Adding commands

Just add new functions in the `commands.py` file and pass them as arguments to the `set_commands` method in `main.py`.
