# TelBot

Telegram chat bot built using the Telegram Bot API.

## Installation

- Get a [Telegram Bot API](https://core.telegram.org/bots/api) token.
- Set your token as a environment variable: `export TELEGRAM_API_TOKEN={your_token}`.
- Clone this repository.
- Inside the repository folder execute: `python3 -m venv .` and then `source bin/activate`.
- Install the requirements: `pip install -r requirements.txt`.

## Usage

To run the bot, execute: `python src/main.py`.

### Adding commands

A command is a function that receives a `Message` object and returns a string or list of strings.
To add a command, create a function and then use one of the following `TelBot` methods to let the bot know how to handle it.

- `on_message_equals`: Executes command when a received message is equal to a given text.
- `on_message_matches`: Executes command when a received message matches a given regular expression.
- `on_message_contains`: Executes command when a received message contains a given text.
- `on_error`: Executes command when another command fails.

#### Examples

- Say hello when a received message contains the words "hi" or "hello".

```python
def hello(message):
    name = message.user_first_name
    return f"Hello {name}!"

bot.on_message_equals(["xkcd"], xkcd)
```

- Make a calculation and return the result, using the [newton API](https://github.com/aunyks/newton-api). When using regular expressions, the capture groups are used as arguments of the message (`message.args`).

```python
def newton(message):
    operation = message.args[0]
    expression = message.args[1]
    response = requests.get(f"https://newton.now.sh/{operation}/{expression}")
    data = response.json()
    return f"The result is {data['result']}"

bot.on_message_matches([r"newton (\w+) (.+)"], newton)
```
