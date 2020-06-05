from commands.codes import command_codes

class Message:

	def __init__(self, user_id, chat_id, content, timestamp):
		pass

	def get_content(self):
		pass

	def get_user_id(self):
		pass

	def get_chat_id(self):
		pass

	def get_timestamp(self):
		pass

	def normalize(self):
		pass

	def uppercase(self):
		pass

	def lowercase(self):
		pass


class TelBot:

	def __init__(self, token):
		"""Telegram Bot's class constructor.
		Receives:
		* token: A valid Telegram Bot API token.
		Returns:
		* TelBot object.
		"""
		pass

	def _make_request(self, endpoint):
		pass

	def send_message(self, chat_id, content, parse_mode=None):
		pass

	def read_messages(self, chat_id):
		pass

	def set_command(self, command):
		pass

	def reset_commands(self):
		pass

	def handle_message(self, message):
		pass
