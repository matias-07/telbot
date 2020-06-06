import os
import random
from telbot import TelBot

TOKEN = os.environ.get("TELEGRAM_API_TOKEN")

def say_hi(**kwargs):
	text = kwargs.get("text")
	user_name = kwargs.get("user_name")

	if "hello" in text or "hi" in text:
		return random.choice([
			f"Hi {user_name}!",
			f"Hey {user_name}, what's up?",
		])

def say_bye(**kwargs):
	text = kwargs.get("text")
	user_name = kwargs.get("user_name")

	if "bye" in text:
		return [
			f"Bye {user_name}!",
			"Take care."
		]

if __name__ == "__main__":
	bot = TelBot(TOKEN)
	bot.set_command(say_hi)
	bot.set_command(say_bye)
	bot.run()
