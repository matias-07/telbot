import os
import random
import requests
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

def btc(**kwargs):
	text = kwargs.get("text").upper().split(" ")
	
	if len(text) != 3:
		return None
	if text[0] != "BTC" or text[1] != "TO":
		return None
	
	query_currency = text[2]

	try:
		response = requests.get("https://bitpay.com/api/rates")
		json_response = response.json()
		for currency in json_response:
			if currency["code"] == query_currency:
				return f"1 BTC = {currency['rate']} {query_currency}"
	except:
		return "Something went wrong..."

	return "Sorry, I couldn't find the conversion to that currency"


if __name__ == "__main__":
	bot = TelBot(TOKEN)

	bot.set_commands(
		say_hi,
		say_bye,
		btc
	)

	bot.run()
