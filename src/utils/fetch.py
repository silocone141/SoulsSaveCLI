import json
import os


def get_data(file_path):
    try:
        with open(file_path, "r") as file:
            config_data = json.load(file)
        return config_data

    except FileNotFoundError:
        raise FileNotFoundError("Config file does not exist. Run 'soulsave "
                                "init' to generate the file")


def write_data(file_path, data):
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)


def get_config_file():
    config_dir = os.getenv("XDG_CONFIG_HOME",
                           os.path.join(os.getenv("HOME"), ".config"))

    return os.path.join(config_dir, "soulsave/config.json")


def resolve_save(profile, path, save, extension):
    save_file = os.path.join(path, profile,
                             f"{save}")

    if not os.path.isfile(save_file):
        save_file = os.path.join(path, profile,
                                 f"{save + extension}")
        if not os.path.isfile(save_file):
            return

    return save_file
