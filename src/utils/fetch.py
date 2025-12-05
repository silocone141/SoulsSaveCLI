import json
import os


class InvalidSaveStatePath(Exception):
    pass


class InvalidSaveFile(Exception):
    pass


class ProfileDoesNotExist(Exception):
    pass


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


def get_config_values(profile=None):
    config_file = get_config_file()
    config_data = get_data(config_file)

    try:
        save_state_path = config_data["save_states"]
        profiles = config_data["profiles"]
        profile_list = list(config_data["profiles"].keys())

    except KeyError:
        raise KeyError(
            "Error reading configuration file. Please review your "
            "configuration or run 'soulsave init' to properly generate "
            "the file."
        )

    if profile is not None:
        if profile not in profile_list:
            raise ProfileDoesNotExist(f"Profile {profile} does not exist. "
                                      "Use 'soulsave new' to create a new "
                                      "profile.")

    for dir_name in profile_list:
        save_file = config_data["profiles"][dir_name]
        if not os.path.isfile(save_file):
            raise InvalidSaveFile(f"Save file for profile '{dir_name}' "
                                  f"does not exist. Value: '{save_file}'")

    if not os.path.isdir(save_state_path):
        raise InvalidSaveStatePath("Configuration option 'save_states' "
                                   "must be a valid directory")
    else:
        return {"save_states": save_state_path, "profiles": profiles}


def resolve_save(profile, path, save, extension):
    save_file = os.path.join(path, profile,
                             f"{save}")

    if not os.path.isfile(save_file):
        save_file = os.path.join(path, profile,
                                 f"{save + extension}")
        if not os.path.isfile(save_file):
            return

    return save_file
