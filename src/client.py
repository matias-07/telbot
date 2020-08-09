import time
import requests
from datetime import datetime

class Message:
    """
    Wrapper class for a Telegram Message Object.
    """
    
    def __init__(self, message_dict):
        self.content = message_dict["text"]
        self.chat_id = message_dict["chat"]["id"]
        self.user_name = message_dict["from"]["first_name"]
        self.timestamp = int(message_dict["date"])
        self.args = []
    
    def __getitem__(self, index):
        return self.content.split()[index]
    
    def __iter__(self):
        pass
    
    def __contains__(self, text):
        return self._normalize(text) in self._normalize(self.content)
    
    def __len__(self):
        return len(self.content.split())
    
    def split(self):
        return self._normalize(self.content).split()
    
    def _normalize(self, text):
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

    def __init__(self, content, to):
        self.content = content
        self.to = to
    
    def is_photo(self):
        if len(self.content.split()) != 1:
            return False

        for extension in [".jpg", ".png", ".jpeg"]:
            if self.content.endswith(extension):
                return True
        
        return False
    
    def is_animation(self):
        return len(self.content.split()) == 1 and self.content.endswith(".gif")
    
    def send(self):
        pass

class BotClient:

    def __init__(self, token):
        self.api_url = "https://api.telegram.org/bot" + token
        self.timestamp = datetime.now().timestamp()

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
        url = f"{self.api_url}/{endpoint}"
        response = None

        if method == "GET":
            response = requests.get(url, params=data)
        elif method == "POST":
            response = requests.post(url, data=data)

        time.sleep(0.25)
        json_response = response.json()

        if not json_response["ok"]:
            return None

        return json_response["result"]
    
    def send_response(self, response):
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
        updates = self.make_request("getUpdates", "GET")
        messages = map(lambda update: update.get("message", {}), updates)
        messages = filter(lambda message: int(message.get("date", 0)) > self.timestamp, messages)
        messages = [Message(message) for message in messages]
        if len(messages) > 0:
            self.timestamp = messages[-1].timestamp
        return messages
    
    def get_me(self):
        return self.make_request("getMe", "GET")

    def __str__(self):
        obj = self.get_me()
        return f"Telegram BotClient - ID: {obj['id']} - Username: {obj['username']}"
