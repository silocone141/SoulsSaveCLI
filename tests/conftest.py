import os

import pytest

from src.utils import fetch
from tests import helpers


# -------
# HELPERS
# -------
def init_tmp_setup(monkeypatch, tmp_path):
    """
    monkeypatch XDG_CONFIG_HOME to tmp_path and returns initial paths needed
    for testing.

    NOTE: Not all fixtures will require all the returned files/paths so that
          task is left to the individual fixtures.
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
        "game_path": game_path
    }


def tmp_conf_setup(tmp_path, profile: str, save_states_path, game_path,
                   create_save_state=True, create_game_save=True):
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


def tmp_env_create(monkeypatch, tmp_path, params=[],
                   create_save_states_dir=True, create_config_dir=True,
                   create_game_saves_dir=True):
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
        "profile_paths": profile_paths
    }


# --------
# FIXTURES
# --------
@pytest.fixture
def set_test_config(monkeypatch, tmp_path):
    params = [
        {
            "name": "happy-path",
            "add_to_config": True,
            "create_save_state": True,
            "create_game_save": True
        },
        {
            "name": "no-game",
            "add_to_config": True,
            "create_save_state": True,
            "create_game_save": False
        }
    ]

    tmp_data = tmp_env_create(monkeypatch, tmp_path, params)
    config_file = tmp_data["config_file"]
    profile_paths = tmp_data["profile_paths"]

    # Happy path directory in save-states/
    happy_save_state_path = profile_paths["happy-path"]["save_state_path"]

    # Noexistent game save file's directory in save-states/
    no_game_save_state_path = profile_paths["no-game"]["save_state_path"]

    # Set return package + config_data
    tmp_data_return = {
        "config_file": config_file,
        "config_data": tmp_data["config_data"],
        "save_states_paths": {
            "happy-path": happy_save_state_path,
            "no-game": no_game_save_state_path
        }
    }

    # Write config file
    fetch.write_data(config_file, tmp_data_return["config_data"])

    return tmp_data_return


@pytest.fixture
def set_test_init(monkeypatch, tmp_path):
    tmp_paths = tmp_env_create(monkeypatch, tmp_path, create_config_dir=False,
                               create_save_states_dir=False,
                               create_game_saves_dir=False)
    config_path = tmp_paths["config_path"]
    config_file = tmp_paths["config_file"]
    save_states_path = tmp_paths["save_states_path"]

    return {"tmp_path": tmp_path, "config_path": config_path,
            "config_file": config_file, "save_states_path": save_states_path}


@pytest.fixture
def set_test_new(monkeypatch, tmp_path):
    tmp_paths = init_tmp_setup(monkeypatch, tmp_path)
    config_path = tmp_paths["config_path"]
    config_file = tmp_paths["config_file"]
    save_states_path = tmp_paths["save_states_path"]
    game_path = tmp_paths["game_path"]

    os.mkdir(config_path)
    os.mkdir(save_states_path)
    os.mkdir(game_path)

    existing_profile = tmp_conf_setup(tmp_path, "existing", save_states_path,
                                      game_path)

    # Set return package
    tmp_data = {
        "config_file": config_file,
        "config_data": {
            "save_states": save_states_path,
            "profiles": {}
        },
        # existing_profile:
        # {"save_state_dir": save_state_dir, "game_save_path": game_save_file}
        "existing_profile": existing_profile
    }

    # Write config file
    fetch.write_data(config_file, tmp_data["config_data"])

    return tmp_data


@pytest.fixture
def set_test_single_valid_profile(monkeypatch, tmp_path):
    """
    Simple test environment that contains exactly one existing, valid profile.
    """
    tmp_paths = init_tmp_setup(monkeypatch, tmp_path)
    config_path = tmp_paths["config_path"]
    config_file = tmp_paths["config_file"]
    save_states_path = tmp_paths["save_states_path"]
    game_path = tmp_paths["game_path"]

    os.mkdir(config_path)
    os.mkdir(save_states_path)
    os.mkdir(game_path)

    existing_profile = tmp_conf_setup(tmp_path, "existing", save_states_path,
                                      game_path)

    # Set return package
    tmp_data = {
        "config_file": config_file,
        "config_data": {
            "save_states": save_states_path,
            "profiles": {
                "existing": existing_profile["game_save_path"]
            }
        },
        # existing_profile:
        # {"save_state_dir": save_state_dir, "game_save_path": game_save_file}
        "existing_profile": existing_profile
    }

    # Write config file
    fetch.write_data(config_file, tmp_data["config_data"])

    return tmp_data
