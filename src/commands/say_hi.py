from command import Command

class SayHiCommand(Command):

	def __init__(self):
		pass

	def execute(self, message):
		result = None

		if "hello" in message:
			result = random.choice([
				f"Hello!",
				f"Hi {message.get_user()}",
				f"I've missed you, {message.get_user()}",
			])

		return self.bot.send_message(message.chat_id, result)
