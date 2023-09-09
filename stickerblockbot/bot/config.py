import json
import os

config_path = os.path.join(os.path.dirname(__file__), "..", "..", "config.json")
config = None


def load_config():
    global config

    try:
        with open(config_path, "r") as jsonfile:
            config = json.load(jsonfile)
    except FileNotFoundError:
        config = {}
        save_config()


def save_config():
    global config
    with open(config_path, "w") as jsonfile:
        json.dump(config, jsonfile)


def get(key):
    global config

    if config is None:
        try:
            load_config()
        except Exception as ex:
            print("Unable to load configuration!\n" + str(ex))
            return None

    if key in config:
        return config[key]

    return None


def set(key, value):
    config[key] = value
    save_config()
