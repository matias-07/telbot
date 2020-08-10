import os
import sys
import commands as cmd
from telbot import TelBot

TELEGRAM_API_TOKEN = os.environ.get("TELEGRAM_API_TOKEN")

if not TELEGRAM_API_TOKEN:
    sys.exit("Telegram API token not found")

bot = TelBot(TELEGRAM_API_TOKEN)
bot.on_error(cmd.error_message)
bot.on_message_contains(["hello", "hi"], cmd.say_hello)
bot.on_message_contains(["bye"], cmd.say_bye)
bot.on_message_contains(["yes or no"], cmd.yesno)
bot.on_message_equals(["xkcd"], cmd.xkcd)
bot.on_message_equals(["reddit"], cmd.reddit)
bot.on_message_matches(["btc to (.+)"], cmd.btc)
bot.on_message_matches(["newton (\\w+) (.+)"], cmd.newton)

if __name__ == "__main__":
    if not bot.is_connected():
        sys.exit("Connection error. The token may be invalid.")
    print("TelBot successfully connected and running!")
    bot.run()
