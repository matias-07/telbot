import requests
import time
import json
from datetime import datetime


class TelBot:
	"""TelBot's main class.

	To use TelBot you will need a valid token for the Bot API:
		https://core.telegram.org/bots/api

	This class is made so you can add any
	command you'd like and then let the bot handle
	everything for you by calling telbot.run().

	"""

	API_URL = "https://api.telegram.org/bot"
	DEBUG = False


	def __init__(self, token):
		"""TelBot's class constructor.

		Parameters
		----------
		token: String
			A valid Telegram Bot API token.

		"""
		self.token = token
		self.timestamp = datetime.now().timestamp()
		self.commands = []


	def set_commands(self, *commands):
		"""Set commands for the bot.

		Parameters
		----------
		commands: One or multiple functions
			Commands the bot will support. Each of these functions
			must return none (None), one (string) or multiple
			(list of strings) responses.

		"""
		self.commands = commands


	def make_request(self, endpoint, method, data={}):
		"""Makes a request to the Telegram Bot API.

		Parameters
		----------
		endpoint: String
			Valid Telegram Bot API endpoint.
		method: String
			HTTP request method, GET or POST.
		data: Dictionary
			Request's query arguments (GET) or JSON data (POST).

		Returns
		-------
		Dictionary
			Response's data.

		"""
		url = f"{self.API_URL}{self.token}/{endpoint}"
		response = None

		if method == "GET":
			response = requests.get(url, params=data)
		elif method == "POST":
			response = requests.post(url, data=data)

		time.sleep(1)
		json_response = response.json()
		
		if self.DEBUG:
			print(" " * 80)
			print("=" * 80)
			print(f"{datetime.now()} - {method} {endpoint} - {response.status_code}")
			print(json.dumps(json_response, indent=4))
			print("=" * 80)
			print(" " * 80)

		if not json_response["ok"]:
			return None

		return json_response["result"]


	def send_message(self, content, **data):
		"""Sends a message.

		Parameters
		----------
		content: String
			Content of the message to be sent. It can be text
			or URL to images.
		**data
			Aditional data to be sent in the request.

		Returns
		-------
		Dictionary
			Response's data.

		"""
		if self._is_photo(content):
			data["photo"] = content
			return self.make_request("sendPhoto", "POST", data)

		if self._is_animation(content):
			data["animation"] = content
			return self.make_request("sendAnimation", "POST", data)

		data["text"] = content
		return self.make_request("sendMessage", "POST", data)


	def get_unread_messages(self):
		"""Fetches unread messages from all chats the bot is part of.

		Returns
		-------
		List
			A list of messages, each represented as a dictionary.

		"""
		updates = self.make_request("getUpdates", "GET")
		if not updates:
			return []

		messages = map(lambda update: update.get("message", {}), updates)
		messages = filter(lambda message: int(message.get("date", 0)) > self.timestamp, messages)

		return list(messages)


	def handle_message(self, text, user_name, chat_id):
		"""Process a message and executes command if found.

		Parameters
		----------
		text: String
			Message's text.
		user_name: String
			Sender's user name.
		chat_id: String
			ID of the chat the message was sent to.

		"""
		for command in self.commands:
			result = command(text=text, user_name=user_name)

			if not result:
				continue

			if isinstance(result, list):
				for message in result:
					self.send_message(message, chat_id=chat_id)
			else:
				self.send_message(result, chat_id=chat_id)


	def read_messages(self):
		"""Reads all unread messages and updates
		the bot's timestamp.
		"""
		for message in self.get_unread_messages():
			text = message["text"]
			user_name = message["from"]["first_name"]
			chat_id = message["chat"]["id"]
			self.handle_message(text, user_name, chat_id)
			self.timestamp = int(message["date"])


	def run(self):
		"""Runs the bot indefinetely.
		"""
		while True:
			self.read_messages()


	def _is_photo(self, content):
		"""Checks if content is a photo.
		"""
		return len(content.split()) == 1 and any(map(
			lambda e: content.endswith(f".{e}"),
			["jpg", "png", "jpeg"]
		))


	def _is_animation(self, content):
		"""Checks if content is an animation.
		"""
		return len(content.split()) == 1 and content.endswith(".gif")
