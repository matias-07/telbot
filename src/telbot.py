import re
from datetime import datetime
from client import BotClient, Response

class TelBot:

    def __init__(self, api_token):
        self.client = BotClient(api_token)
        self.commands = []
        self.programmed = []
        self.error_response = lambda: "Sorry, something went wrong."

    def __str__(self):
        return str(self.client)

    def is_connected(self):
        return self.client.get_me()

    def on_message_contains(self, keywords, command):
        def wrapper(message):
            for keyword in keywords:
                if keyword in message:
                    return command(message)
        self.commands.append(wrapper)

    def on_message_equals(self, keywords, command):
        def wrapper(message):
            for keyword in keywords:
                if message.content.lower() == keyword.lower():
                    return command(message)
        self.commands.append(wrapper)

    def on_message_matches(self, expressions, command):
        def wrapper(message):
            for exp in expressions:
                match = re.search(exp, message.content.lower())
                if match:
                    message.args = list(match.groups())
                    return command(message)
        self.commands.append(wrapper)

    def on_error(self, command):
        self.error_response = command

    def handle_message(self, message):
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
            for result in results:
                response = Response(result, message.chat_id)
                self.client.send_response(response)

    def read_inbox(self):
        for message in self.client.fetch_messages():
            self.handle_message(message)    

    def run(self):
        while True:
            self.read_inbox()
