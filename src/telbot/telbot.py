import requests
import time
import json
import telbot.utils as utils
from datetime import datetime


class TelBot:

	DEBUG = False

	def __init__(self, token):
		"""Telegram Bot's class constructor.
		Receives:
		* token: A valid Telegram Bot API token.
		Returns:
		* TelBot object.
		"""
		self.token = token
		self.timestamp = datetime.now().timestamp()
		self.commands = []


	def set_commands(self, *commands):
		self.commands = commands


	def make_request(self, endpoint, method, data={}):
		"""Makes a request to the Telegram Bot API and
		returns the JSON response.
		Receives:
		* endpoint: String.
		* method: String ("GET", "POST")
		* data: Dictionary.
		Returns:
		* Response.
		"""
		url = f"https://api.telegram.org/bot{self.token}/{endpoint}"
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
		if utils.is_photo(content):
			data["photo"] = content
			return self.make_request("sendPhoto", "POST", data)

		data["text"] = content
		return self.make_request("sendMessage", "POST", data)


	def get_unread_messages(self):
		updates = self.make_request("getUpdates", "GET")
		if not updates:
			return []

		messages = map(lambda update: update["message"], updates)
		messages = filter(lambda message: int(message["date"]) > self.timestamp, messages)

		return list(messages)


	def handle_message(self, text, user_name, chat_id):
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
		for message in self.get_unread_messages():
			text = message["text"]
			user_name = message["from"]["first_name"]
			chat_id = message["chat"]["id"]
			self.handle_message(text, user_name, chat_id)
			self.timestamp = int(message["date"])


	def run(self):
		while True:
			self.read_messages()
