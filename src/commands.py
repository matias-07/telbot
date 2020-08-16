import random
import requests
from telbot import cache

def error_message():
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
    user_first_name = message.user_first_name
    return random.choice([
        f"Hi {user_first_name}!",
        f"Hey {user_first_name}, what's up?",
        f"Long time no see {user_first_name}",
    ])

def say_bye(message):
    """Returns a goodbye.
    """
    user_first_name = message.user_first_name
    return random.choice([
        f"Bye {user_first_name}!",
        f"See you later {user_first_name}",
        f"Take care {user_first_name}",
    ])

def xkcd(message):
    """Returns a random xkcd comic [title, image].
    """
    comic_id = random.randint(1, 2316)
    response = requests.get(f"https://xkcd.com/{comic_id}/info.0.json")
    response.raise_for_status()
    data = response.json()
    return [data.get("title"), data.get("img")]

def btc(message):
    """Returns BTC conversion to given currency.
    """
    currency = message.args[0].upper()
    response = requests.get("https://bitpay.com/api/rates")
    response.raise_for_status()
    data = response.json()
    for _currency in data:
        if _currency["code"] == currency:
            return f"1 BTC = {_currency['rate']} {currency}"

def newton(message):
    """Makes a math operation and returns the result.
    Reference: https://github.com/aunyks/newton-api
    """
    operation = message.args[0]
    expression = message.args[1]
    response = requests.get(f"https://newton.now.sh/{operation}/{expression}")
    response.raise_for_status()
    data = response.json()
    return f"The result is {data['result']}"

def reddit(message):
    """Returns a top reddit post [message, url].
    """
    data = cache.get("reddit")
    if not data:
        response = requests.get(
            "https://www.reddit.com/.json",
            headers={"User-agent": "TelBot 0.1"}
        )
        response.raise_for_status()
        data = response.json()
        cache.set("reddit", data, 60 * 60)
    posts = data["data"]["children"]
    post = random.choice(posts)
    return f"https://www.reddit.com/{post['data']['permalink']}"

def yesno(message):
    """Returns yes or no as a GIF.
    """
    response = requests.get(f"https://yesno.wtf/api")
    response.raise_for_status()
    json_response = response.json()
    return json_response["image"]
