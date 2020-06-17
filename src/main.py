import os
from telbot import TelBot
from commands import *

TOKEN = os.environ.get("TELEGRAM_API_TOKEN")

if __name__ == "__main__":
	bot = TelBot(TOKEN)
	print(">> TelBot correctly initialized!")
	bot.set_commands(
		say_hi,
		say_bye,
		btc,
		xkcd,
		reddit,
		newton,
		yesno
	)

	bot.run()
