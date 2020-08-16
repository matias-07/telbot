#!/usr/bin/env python3

import os
import sys
import utils
import commands as cmd
from telbot import TelBot

token = os.environ.get("TELEGRAM_API_TOKEN")

if not token:
    sys.exit("Token not found")

bot = TelBot(token)
bot.on_error(cmd.error_message)
bot.on_message_contains(["hello", "hi"], cmd.say_hello)
bot.on_message_contains(["bye"], cmd.say_bye)
bot.on_message_contains(["yes or no"], cmd.yesno)
bot.on_message_equals(["xkcd"], cmd.xkcd)
bot.on_message_equals(["reddit"], cmd.reddit)
bot.on_message_matches(["btc to (.+)"], cmd.btc)
bot.on_message_matches([r"newton (\w+) (.+)"], cmd.newton)

if __name__ == "__main__":
    try:
        utils.log("Starting bot...")
        for message in bot.run():
            utils.log(message)
    except KeyboardInterrupt:
        utils.log("Stopping bot...", True)
        sys.exit(0)
