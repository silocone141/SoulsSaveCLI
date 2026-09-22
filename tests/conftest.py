import os

import pytest
from src.utils import fetch

from tests import helpers

# TODO Normalize output strings (e.g. load vs. add success output)


# -------
# HELPERS
# -------
def init_tmp_setup(monkeypatch, tmp_path):
    """
    monkeypatch XDG_CONFIG_HOME to tmp_path and returns initial paths needed
    for testing.
    """
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))

    config_path = os.path.join(tmp_path, "soulsave")
    config_file = os.path.join(tmp_path, "soulsave/config.json")
    save_states_path = os.path.join(tmp_path, "save-states")
    game_path = os.path.join(tmp_path, "game")

    return {
        "config_file": config_file,
        "config_path": config_path,
        "save_states_path": save_states_path,
        "game_path": game_path,
    }


def tmp_conf_setup(tmp_path, profile: str, save_states_path, game_path,
                   create_save_state=True, create_game_save=True):
    """

    """
    save_state_dir = os.path.join(save_states_path, profile)
    save_state_file = os.path.join(save_state_dir, "saved-state.txt")
    game_save_dir = os.path.join(game_path, profile)
    game_save_file = os.path.join(game_save_dir, "save-file.txt")

    if create_save_state:
        os.mkdir(save_state_dir)
        helpers.write_txt(save_state_file, "Saved state content")

    if create_game_save:
        os.mkdir(game_save_dir)
        helpers.write_txt(game_save_file, "Live game save")

    return {"save_state_dir": save_state_dir, "game_save_path": game_save_file}


def tmp_env_create(monkeypatch, tmp_path, params=None,
                   create_save_states_dir=True, create_config_dir=True,
                   create_game_saves_dir=True):
    """

    """
    tmp_paths = init_tmp_setup(monkeypatch, tmp_path)
    config_path = tmp_paths["config_path"]
    config_file = tmp_paths["config_file"]
    save_states_path = tmp_paths["save_states_path"]
    game_path = tmp_paths["game_path"]
    config_data = {"save_states": save_states_path, "profiles": {}}
    profile_paths = {}

    if create_save_states_dir:
        os.mkdir(save_states_path)

    if create_game_saves_dir:
        os.mkdir(game_path)

    if params is None:
        params = []

    for profile in params:
        profile_name = profile["name"]
        profile_game_path = os.path.join(game_path, profile_name,
                                         "save-file.txt")
        profile_save_state_dir = os.path.join(save_states_path, profile_name)

        profile_paths[profile_name] = {}
        profile_paths[profile_name]["save_state_path"] = profile_save_state_dir
        profile_paths[profile_name]["game_save_file"] = profile_game_path

        if profile["add_to_config"]:
            config_data["profiles"][profile_name] = profile_game_path

        tmp_conf_setup(tmp_path, profile_name, save_states_path, game_path,
                       create_save_state=(profile["create_save_state"] and
                                          create_save_states_dir),
                       create_game_save=(profile["create_game_save"] and
                                         create_game_saves_dir))

    if create_config_dir:
        os.mkdir(config_path)

    return {
        "config_data": config_data,
        "config_file": config_file,
        "config_path": config_path,
        "save_states_path": save_states_path,
        "game_path": game_path,
        "profile_paths": profile_paths,
    }


# --------
# FIXTURES
# --------
@pytest.fixture
def set_test_single_valid_profile(monkeypatch, tmp_path):
    """
    Simple test environment that contains exactly one existing, valid profile.
    """
    params = [
        {
            "name": "existing",
            "add_to_config": True,
            "create_save_state": True,
            "create_game_save": True,
        },
    ]
    tmp_data = tmp_env_create(monkeypatch, tmp_path, params)
    config_data = tmp_data["config_data"]
    config_file = tmp_data["config_file"]

    tmp_data_return = {
        "config_file": config_file,
        "config_data": config_data,
        "profile_paths": tmp_data["profile_paths"]["existing"],
    }

    fetch.write_data(config_file, tmp_data_return["config_data"])

    return tmp_data_return


@pytest.fixture
def set_test_invalid_save_file(monkeypatch, tmp_path):
    params = [
        {
            "name": "happy-path",
            "add_to_config": True,
            "create_save_state": True,
            "create_game_save": True,
        },
        {
            "name": "no-game",
            "add_to_config": True,
            "create_save_state": True,
            "create_game_save": False,
        },
    ]
    tmp_data = tmp_env_create(monkeypatch, tmp_path, params)
    config_file = tmp_data["config_file"]
    profile_paths = tmp_data["profile_paths"]
    happy_save_state_path = profile_paths["happy-path"]["save_state_path"]
    no_game_save_state_path = profile_paths["no-game"]["save_state_path"]

    tmp_data_return = {
        "config_file": config_file,
        "config_data": tmp_data["config_data"],
        "save_states_paths": {
            "happy-path": happy_save_state_path,
            "no-game": no_game_save_state_path
        },
    }

    fetch.write_data(config_file, tmp_data_return["config_data"])

    return tmp_data_return


@pytest.fixture
def set_test_init(monkeypatch, tmp_path):
    # Do not create $XDG_CONFIG_HOME/soulsave or the save state directories
    tmp_paths = tmp_env_create(monkeypatch, tmp_path, create_config_dir=False,
                               create_save_states_dir=False,
                               create_game_saves_dir=False)
    config_path = tmp_paths["config_path"]
    config_file = tmp_paths["config_file"]
    save_states_path = tmp_paths["save_states_path"]

    return {"tmp_path": tmp_path, "config_path": config_path,
            "config_file": config_file, "save_states_path": save_states_path}


@pytest.fixture
def set_test_new_no_mkdir(monkeypatch, tmp_path):
    params = [
        {
            "name": "existing",
            "add_to_config": False,
            "create_save_state": True,
            "create_game_save": True,
        },
    ]
    tmp_data = tmp_env_create(monkeypatch, tmp_path, params)
    config_file = tmp_data["config_file"]
    config_data = tmp_data["config_data"]

    tmp_data = {
        "config_file": config_file,
        "config_data": config_data,
        "profile_paths": tmp_data["profile_paths"]
    }
    fetch.write_data(config_file, config_data)

    return tmp_data


@pytest.fixture
def set_test_trash(monkeypatch, tmp_path):
    params = [
        {
            "name": "confirm",
            "add_to_config": True,
            "create_save_state": True,
            "create_game_save": True,
        },
        {
            "name": "silent",
            "add_to_config": True,
            "create_save_state": True,
            "create_game_save": True,
        },
    ]
    tmp_data = tmp_env_create(monkeypatch, tmp_path, params)
    config_file = tmp_data["config_file"]
    profile_paths = tmp_data["profile_paths"]

    confirm_saves = profile_paths["confirm"]["save_state_path"]
    silent_saves = profile_paths["silent"]["save_state_path"]

    tmp_data_return = {
        "config_file": config_file,
        "config_data": tmp_data["config_data"],
        "save_states_paths": {
            "confirm": confirm_saves,
            "silent": silent_saves,
        },
    }
    fetch.write_data(config_file, tmp_data_return["config_data"])

    return tmp_data_return
