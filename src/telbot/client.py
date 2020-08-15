import time
import requests
from datetime import datetime

class Message:
    """Wrapper class for a Telegram Message Object.
    """

    def __init__(self, message_dict):
        """Constructor of the Message class.
        Parameters:
        message_dict -- Message object received from the Telegram Bot API.
        """
        self.content = message_dict["text"]
        self.chat_id = message_dict["chat"]["id"]
        self.user_name = message_dict["from"]["first_name"]
        self.timestamp = int(message_dict["date"])
        self.args = []

    def __getitem__(self, index):
        """Returns the word in the message content
        in the given index.
        """
        return self.content.split()[index]

    def __contains__(self, text):
        """Returns a boolean indicating if the given text
        (normalized) is present in the message content.
        """
        return self._normalize(text) in self._normalize(self.content)

    def __len__(self):
        """Returns the length of the message content.
        """
        return len(self.content)

    def split(self):
        """Splits the message content (normalized) in
        words and returns the resulting list.
        """
        return self._normalize(self.content).split()

    def _normalize(self, text):
        """Returns the normalized version of the given text
        (lowercase, no diacritics).
        """
        diacritics = {
            "á": "a",
            "é": "e",
            "í": "i",
            "ó": "o",
            "ú": "u",
        }
        normalized = ""
        for character in text.lower():
            if character in diacritics:
                normalized += diacritics[character]
            else:
                normalized += character
        return normalized

class Response:
    """Represents a response message.
    """

    def __init__(self, content, to):
        """Constructor of the Response class.
        Parameters:
        content -- Response content.
        to -- Destinatary chat_id
        """
        self.content = content
        self.to = to

    def is_photo(self):
        """Returns a boolean indicating if the response
        is a photo.
        """
        if len(self.content.split()) != 1:
            return False

        for extension in [".jpg", ".png", ".jpeg"]:
            if self.content.endswith(extension):
                return True

        return False

    def is_animation(self):
        """Returns a boolean indicating if the response
        is an animation.
        """
        return len(self.content.split()) == 1 and self.content.endswith(".gif")

class BotClient:
    """Wrapper for the Telegram Bot API.
    """

    SLEEP_TIME = 0.25 # Sleep time after each request.

    def __init__(self, token):
        """Constructor of the BotClient class.
        Parameters:
        token -- Valid Telegram Bot API token
        """
        self.api_url = "https://api.telegram.org/bot" + token
        self.timestamp = datetime.now().timestamp()

    def make_request(self, endpoint, method, data={}):
        """Makes a request to the Telegram Bot API and
        returns the response as a dictionary.

        Parameters:
        endpoint -- Valid Telegram Bot API endpoint.
        method -- HTTP request method, GET or POST.
        data -- Request's query arguments (GET) or JSON data (POST).
        """
        url = f"{self.api_url}/{endpoint}"
        response = None
        if method == "GET":
            response = requests.get(url, params=data)
        elif method == "POST":
            response = requests.post(url, data=data)
        time.sleep(self.SLEEP_TIME)
        json_response = response.json()
        if not json_response["ok"]:
            return None
        return json_response["result"]

    def send_response(self, response):
        """Sends a response.
        Parameters:
        response -- Response object
        """
        data = {"chat_id": response.to}

        if response.is_photo():
            data["photo"] = response.content
            return self.make_request("sendPhoto", "POST", data)
        elif response.is_animation():
            data["animation"] = response.content
            return self.make_request("sendAnimation", "POST", data)
        else:
            data["text"] = response.content
            return self.make_request("sendMessage", "POST", data)

    def fetch_messages(self):
        """Returns all the received messages since the last
        fetch or the bot starting time.
        """
        updates = self.make_request("getUpdates", "GET")
        messages = map(lambda update: update.get("message", {}), updates)
        messages = filter(lambda message: int(message.get("date", 0)) > self.timestamp, messages)
        messages = [Message(message) for message in messages]
        if len(messages) > 0:
            self.timestamp = messages[-1].timestamp
        return messages

    def get_me(self):
        """Returns information about the bot user.
        """
        return self.make_request("getMe", "GET")
