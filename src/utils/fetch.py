import json
import os


def get_data(file_path):
    try:
        with open(file_path, "r") as file:
            config_data = json.load(file)
        return config_data

    except FileNotFoundError:
        return {}


def write_data(file_path, data):
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)


def get_config_dir():
    config_dir = os.getenv("XDG_CONFIG_HOME",
                           os.path.join(os.getenv("HOME"), ".config"))

    return os.path.join(config_dir, "soulsave")


def get_config_file():
    return os.path.join(get_config_dir(), "config.json")
