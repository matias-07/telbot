import random
import requests
from cache import Cache

CACHE = Cache()

def _error_message():
    """Returns a generic error message.
    """
    return random.choice([
        "Oops... An error has ocurred",
        "Something went wrong...",
        "Sorry, I couldn't get that",
    ])

def say_hello(message):
    """Returns a greeting.
    """
    user_name = message.user_name

    return random.choice([
        f"Hi {user_name}!",
        f"Hey {user_name}, what's up?",
    ])


def say_bye(message):
    """Returns a goodbye.
    """
    user_name = message.user_name

    return [
        f"Bye {user_name}",
        "Take care!"
    ]

def xkcd(message):
    """Returns a random xkcd comic [title, image].
    """
    try:
        response = requests.get(f"https://xkcd.com/{random.randint(1, 2316)}/info.0.json")
        json_response = response.json()
        return [
            json_response.get("title"),
            json_response.get("img")
        ]
    except:
        return "Something went wrong..."

def btc(message):
    """Returns BTC conversion to given currency.
    """
    query_currency = message.args[0].upper()

    try:
        response = requests.get("https://bitpay.com/api/rates")
        json_response = response.json()
        for currency in json_response:
            if currency["code"] == query_currency:
                return f"1 BTC = {currency['rate']} {query_currency}"
    except:
        return "Error"

    return "I couldn't find the conversion to that currency"

def newton(message):
    operation = message.args[0]
    expression = message.args[1]

    try:
        response = requests.get(f"https://newton.now.sh/{operation}/{expression}")
        json_response = response.json()
        return f"The result is {json_response['result']}"
    except:
        return _error_message()

def reddit(message):
    """Returns a top reddit post [message, url].
    """
    try:
        json_response = CACHE.get("reddit")

        if not json_response:
            response = requests.get(
                "https://www.reddit.com/.json",
                headers={"User-agent": "TelBot 0.1"}
            )
            json_response = response.json()
            # Cache for 1 hour
            CACHE.set("reddit", json_response, 60 * 60)

        posts = json_response["data"]["children"]
        post = random.choice(posts)
        return f"https://www.reddit.com/{post['data']['permalink']}"
    except:
        return _error_message()

def yesno(message):
    try:
        response = requests.get(f"https://yesno.wtf/api")
        json_response = response.json()
        return json_response["image"]
    except:
        return _error_message()
