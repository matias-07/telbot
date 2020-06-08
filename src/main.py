import os
import random
import requests
from telbot import TelBot
from telbot import Cache


TOKEN = os.environ.get("TELEGRAM_API_TOKEN")
CACHE = Cache()


def _error_message():
	"""Returns a generic error message.
	"""
	return random.choice([
		"Oops... An error has ocurred",
		"Something went wrong...",
		"Sorry, I couldn't get that",
	])


def say_hi(**kwargs):
	"""Returns a greeting.
	"""
	text = kwargs.get("text").lower()
	user_name = kwargs.get("user_name")

	if "hello" in text or "hi" in text:
		return random.choice([
			f"Hi {user_name}!",
			f"Hey {user_name}, what's up?",
		])


def say_bye(**kwargs):
	"""Returns a goodbye.
	"""
	text = kwargs.get("text")
	user_name = kwargs.get("user_name")

	if "bye" in text:
		return [
			f"Bye {user_name}!",
			"Take care."
		]


def btc(**kwargs):
	"""Returns BTC conversion to given currency.
	"""
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
		return _error_message()

	return "I couldn't find the conversion to that currency"


def xkcd(**kwargs):
	"""Returns a random xkcd comic [title, image].
	"""
	if kwargs.get("text").lower() != "xkcd":
		return None

	try:
		response = requests.get(f"https://xkcd.com/{random.randint(1, 2316)}/info.0.json")
		json_response = response.json()
		return [
			json_response.get("title"),
			json_response.get("img")
		]
	except:
		return _error_message()


def reddit(**kwargs):
	"""Returns a top reddit post [message, url].
	"""
	if kwargs.get("text").lower() != "reddit":
		return None

	try:
		json_response = CACHE.get("reddit")

		if not json_response:
			response = requests.get(
				"https://www.reddit.com/.json",
				headers={"User-agent": "TelBot 0.1"}
			)
			json_response = response.json()
			CACHE.set("reddit", json_response, 60 * 60) # Cache for 1 hour

		posts = json_response["data"]["children"]
		post = random.choice(posts)
		return [
			"I recommend this post",
			f"https://www.reddit.com/{post['data']['permalink']}"
		]
	except:
		return _error_message()


if __name__ == "__main__":
	bot = TelBot(TOKEN)
	print(">> TelBot correctly initialized!")
	bot.set_commands(
		say_hi,
		say_bye,
		btc,
		xkcd,
		reddit
	)

	bot.run()
