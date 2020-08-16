import re
from .client import BotClient
from .client import Response
from .client import TelegramBotAPIException

class TelBot:
    """Represents a Telegram bot.
    """

    def __init__(self, api_token):
        """Constructor of the TelBot class.
        Parameters:
        api_token -- A Telegram BOT API token
        """
        self.client = BotClient(api_token)
        self.commands = []
        self.error_response = lambda: "Sorry, something went wrong."

    def is_connected(self):
        """Returns a boolean indicating if the connection
        was successful.
        """
        return self.client.get_me() is not None

    def on_message_contains(self, keywords, command):
        """Sets a command to execute when a message containing
        the given keywords is received.
        Parameters:
        keywords -- List of keywords
        command -- Command function
        """
        def wrapper(message):
            for keyword in keywords:
                if keyword in message:
                    return command(message)
        self.commands.append(wrapper)

    def on_message_equals(self, keywords, command):
        """Sets a command to execute when receiving a message
        equal to any of the given keywords.
        Parameters:
        keywords -- List of keywords
        command -- Command function
        """
        def wrapper(message):
            for keyword in keywords:
                if message.content.lower() == keyword.lower():
                    return command(message)
        self.commands.append(wrapper)

    def on_message_matches(self, expressions, command):
        """Sets a command to execute when receiving a message
        that matches any of the given regular expressions.
        Parameters:
        expressions -- List of regular expressions
        command -- Command function
        """
        def wrapper(message):
            for exp in expressions:
                match = re.search(exp, message.content.lower())
                if match:
                    message.args = list(match.groups())
                    return command(message)
        self.commands.append(wrapper)

    def on_error(self, command):
        """Sets a command to execute when another command
        triggers an error.
        Parameters:
        command -- Command function
        """
        self.error_response = command

    def handle_message(self, message):
        """Reads the given message and executes a command,
        if any, and returns the results.
        Parameters:
        message -- A Message object.
        """
        results = []
        for command in self.commands:
            try:
                results = command(message)
            except:
                results = self.error_response()
            if results:
                if isinstance(results, str):
                    results = [results]
                break
        return [Response(res, message.chat_id) for res in results]

    def run(self):
        """Runs the bot and yields the incoming messages
        and sent responses.
        """
        while True:
            try:
                for message in self.client.fetch_messages():
                    yield message
                    for response in self.handle_message(message):
                        self.client.send_response(response)
                        yield response
            except TelegramBotAPIException as e:
                yield e
