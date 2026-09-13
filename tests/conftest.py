import json
import os
from pathlib import Path

import pytest

from tests import helpers


# -------
# HELPERS
# -------
def init_tmp_setup(monkeypatch, tmp_path):
    """
    monkeypatches XDG_CONFIG_HOME to tmp_path and returns initial paths needed
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
        Path(save_state_file).touch()
        helpers.write_txt(save_state_file, "Saved state content")

    if create_game_save:
        os.mkdir(game_save_dir)
        Path(game_save_file).touch()
        helpers.write_txt(game_save_file, "Live game save")

    return {"save_state_dir": save_state_dir, "game_save_path": game_save_file}


# --------
# FIXTURES
# --------
@pytest.fixture
def set_test_config(monkeypatch, tmp_path):
    tmp_paths = init_tmp_setup(monkeypatch, tmp_path)
    config_path = tmp_paths["config_path"]
    config_file = tmp_paths["config_file"]
    save_states_path = tmp_paths["save_states_path"]
    game_path = tmp_paths["game_path"]

    os.mkdir(config_path)
    os.mkdir(save_states_path)
    os.mkdir(game_path)

    # Happy path setup
    happy_conf = tmp_conf_setup(tmp_path, "happy-path", save_states_path,
                                game_path)
    happy_game_path = happy_conf["game_save_path"]

    # Create save-state with nonexistant game
    no_game_conf = tmp_conf_setup(tmp_path, "no-game", save_states_path,
                                  game_path, create_game_save=False)
    no_game_path = no_game_conf["game_save_path"]

    # Set return package + config_data
    tmp_data = {
        "config_file": config_file,
        "config_data": {
            "save_states": save_states_path,
            "profiles": {
                "happy-path": happy_game_path,
                "no-game": no_game_path
            }
        },
        "save_states_paths": {
            "happy-path": happy_conf["save_state_dir"],
            "no-game": no_game_conf["save_state_dir"]
        }
    }

    # Write config file
    with open(config_file, "w") as file:
        json.dump(tmp_data["config_data"], file)

    return tmp_data


@pytest.fixture
def set_test_init(monkeypatch, tmp_path):
    tmp_paths = init_tmp_setup(monkeypatch, tmp_path)
    config_path = tmp_paths["config_path"]
    config_file = tmp_paths["config_file"]
    save_states_path = tmp_paths["save_states_path"]

    os.mkdir(config_path)

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
    with open(config_file, "w") as file:
        json.dump(tmp_data["config_data"], file)

    return tmp_data
