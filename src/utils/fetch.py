import json
import os


class InvalidSaveStatePath(Exception):
    pass


class InvalidSaveFile(Exception):
    pass


class ProfileDoesNotExist(Exception):
    pass


def get_data(path):
    try:
        with open(path, "r") as file:
            config_data = json.load(file)
        return config_data

    except FileNotFoundError:
        raise FileNotFoundError("Config file does not exist. Run 'soulsave "
                                "init' to generate the file")


def write_data(path, data):
    with open(path, "w") as file:
        json.dump(data, file, indent=4)


def get_config_file():
    """
    Return path to configuration file
    """

    config_dir = os.getenv("XDG_CONFIG_HOME",
                           os.path.join(os.getenv("HOME"), ".config"))

    return os.path.join(config_dir, "soulsave/config.json")


def get_config_values(profile=None):
    """
    Validate configuration values and raise exception if error is found. If the
    configuration file is valid, return configuration values.

    A profile can be passed for profile-specific validations.
    """

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
    """
    Given a profile, the path to the game's save file, save file name (with or
    without extension), and the save file extension return the path to the
    game's save file. If save file does not exist, return None.

    Allows for save file name with extension to be passed to --save-state
    options
    """

    save_file = os.path.join(path, profile,
                             f"{save}")

    if not os.path.isfile(save_file):
        save_file = os.path.join(path, profile,
                                 f"{save + extension}")
        if not os.path.isfile(save_file):
            return

    return save_file
