import re
from datetime import datetime
from .client import BotClient, Response

class TelBot:
    """Represents a Telegram bot.
    """

    def __init__(self, api_token):
        """
        Constructor of the TelBot class.
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
        for command in self.commands:
            results = None
            try:
                results = command(message)
            except:
                results = self.error_response()
            if not results:
                continue
            if isinstance(results, str):
                results = [results]
            return results
        return []

    def handle_inbox(self):
        """Reads the received messages and sends
        the responses.
        """
        for message in self.client.fetch_messages():
            results = self.handle_message(message)
            for result in results:
                response = Response(result, message.chat_id)
                self.client.send_response(response)

    def run(self):
        """Starts the bot.
        """
        while True:
            self.handle_inbox()
