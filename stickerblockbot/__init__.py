import logging
from .bot import start_bot, config, BotTokenException


def main():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)

    try:
        config.load_config()
    except Exception as ex:
        print("Unable to load configuration; exiting! Error was: " + str(ex))
        exit(1)

    token = config.get("token")

    if token is None:
        print("The bot token has not been set. Please enter the bot token given by Telegram:")
        while token is None:
            new_token = input()
            if len(new_token) == 0:
                print("Invalid token. Please try again:")
            else:
                token = new_token
                config.set("token", token)
    else:
        if type(token).__name__ != "str" or len(token) == 0:
            print("Token is not valid. Please check app configuration. Exiting!")
            exit(1)

    try:
        start_bot(token)
    except BotTokenException:
        print("The Telegram token was rejected. Removing stored token and exiting!")
        config.set("token", None)
        exit(1)
